import logging
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.service.sync_resolution_service import SyncResolutionService
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress


logger = logging.getLogger(__name__)


class ProgressUpdater:
    """
    Updates Progress records based on sync event types.

    Handles the logic for updating different progress metrics
    based on the event type. For xapi_statement events, student_id
    and segment_level_id are resolved from the payload and sync
    session chain rather than expected directly in the payload.
    """

    def __init__(
        self,
        db: AsyncSession,
        resolution_service: Optional[SyncResolutionService] = None,
    ):
        """
        Initialize the progress updater.

        Args:
            db: AsyncSession for database operations
            resolution_service: Optional SyncResolutionService for entity resolution chain.
                If not provided, a default instance is created.
        """
        self.db = db
        self.repository = ProgressRepository(db)
        self._resolution_service = resolution_service or SyncResolutionService(db)

    async def update(self, event: SyncEvent) -> None:
        """
        Update progress based on the event type.

        Args:
            event: The sync event to process
        """
        payload = event.payload or {}

        # Resolve student_id from the sync session chain (most reliable).
        # The game sends actor_id=user_id in the payload, but progresses
        # FK references students.id — the chain resolves the correct one.
        student_id = await self._resolve_student_id(event)
        if not student_id:
            # Fall back to payload values if chain resolution fails
            student_id = payload.get("student_id") or payload.get("actor_id")

        # Resolve segment_level_id from payload or via sync session chain
        segment_level_id = payload.get("segment_level_id")
        if not segment_level_id:
            segment_level_id = await self._resolve_segment_level_id(event)

        if not student_id or not segment_level_id:
            logger.warning(
                f"Missing student_id or segment_level_id in event {event.id}"
            )
            return

        progress = await self.repository.get_by_student_and_segment(
            student_id=student_id,
            segment_level_id=segment_level_id,
        )

        if not progress:
            logger.info(
                f"Creating new progress record for student {student_id}, segment_level {segment_level_id}"
            )
            # Try to create, handle duplicate exception
            try:
                progress = await self._create_progress(student_id, segment_level_id)
            except Exception as e:
                # If creation fails due to duplicate, try to get existing one
                logger.warning(
                    f"Failed to create progress, trying to get existing: {str(e)}"
                )
                progress = await self.repository.get_by_student_and_segment(
                    student_id=student_id,
                    segment_level_id=segment_level_id,
                )
                if not progress:
                    logger.error(
                        f"Could not find or create progress for student {student_id}, segment_level {segment_level_id}"
                    )
                    return

        update_data = self._build_update_data(event)
        if update_data:
            await self.repository.update(progress.id, update_data)
            await self.db.commit()
            logger.info(f"Updated progress {progress.id} for event {event.id}")



    def _build_update_data(self, event: SyncEvent) -> dict[str, Any]:
        """
        Build update data based on event type.

        Args:
            event: The sync event

        Returns:
            dict: The update data
        """
        payload = event.payload or {}
        update_data = {}

        event_type = event.event_type

        if event_type == "attempt":
            update_data["attempt_count"] = payload.get("count", 1)

        elif event_type == "error":
            current_errors = payload.get("count", 1)
            update_data["error_count"] = current_errors
            update_data["errors_details"] = payload.get("details")

        elif event_type == "hint_used":
            hints_count = payload.get("count", 1)
            update_data["hints_used_count"] = hints_count

        elif event_type == "score":
            update_data["efficiency_rating"] = payload.get("rating", 0)

        elif event_type == "level_completed":
            update_data["objectives_completed"] = payload.get("count", 1)

        elif event_type == "xapi_statement":
            # Extract progress data from xAPI statement payload
            result = payload.get("result", {})
            verb_id = payload.get("verb_id", "")

            # Level completed/attempted: update based on result
            if "completed" in verb_id or "attempted" in verb_id:
                if result.get("completion") or result.get("success"):
                    update_data["objectives_completed"] = 1

                # Map score to efficiency_rating (0-100 scale)
                score = result.get("score_scaled") or result.get("score_raw")
                if score is not None:
                    if isinstance(score, float) and score <= 1.0:
                        update_data["efficiency_rating"] = int(score * 100)
                    else:
                        update_data["efficiency_rating"] = int(score)

        elif event_type == "raw_stats":
            # Bulk stats update - includes all metrics in one event
            update_data["attempt_count"] = payload.get("attempt_count", 0)
            update_data["error_count"] = payload.get("error_count", 0)
            update_data["hints_used_count"] = payload.get("hints_used_count", 0)
            update_data["errors_details"] = payload.get("errors_details")
            update_data["efficiency_rating"] = int(payload.get("efficiency_rating") or 0)
            update_data["objectives_completed"] = payload.get("objectives_completed", 0)

        elif event_type == "level_time":
            pass

        elif event_type == "difficulty_changed":
            pass

        elif event_type == "adaptation":
            pass

        return update_data

    async def _resolve_student_id(self, event: SyncEvent) -> Optional[UUID]:
        """
        Resolve student_id from the sync session chain via SyncResolutionService.

        Traverses: SyncEvent → SyncSession → GameInstance → student_id

        Args:
            event: The sync event to resolve student_id for

        Returns:
            UUID of the Student, or None if it cannot be resolved
        """
        return await self._resolution_service.resolve_student_id(event.sync_session_id)

    async def _resolve_segment_level_id(self, event: SyncEvent) -> Optional[UUID]:
        """
        Resolve segment_level_id from payload or sync session chain.

        Two resolution paths:
          Path 1: xapi_statement events with object_type/object_id
          Path 2: raw_stats events with segment_id (int)

        Both delegate to SyncResolutionService for the chain traversal:
          SyncEvent → SyncSession → GameInstance → Level → SegmentLevel

        Args:
            event: The sync event to resolve segment_level_id for

        Returns:
            UUID of the SegmentLevel, or None if it cannot be resolved
        """
        payload = event.payload or {}

        # Path 1: xapi_statement with object_type/object_id
        object_type = payload.get("object_type")
        object_id = payload.get("object_id")
        if object_type in ("level", "activity") and object_id:
            try:
                level_number = int(object_id)
            except (ValueError, TypeError):
                logger.warning(
                    f"Cannot parse object_id '{object_id}' as level number in event {event.id}"
                )
                return None
            return await self._resolution_service.resolve_segment_level_id_from_object(
                event.sync_session_id, level_number
            )

        # Path 2: raw_stats with segment_id (maps to Level.level_number)
        segment_id = payload.get("segment_id")
        if segment_id is not None:
            try:
                level_number = int(segment_id)
            except (ValueError, TypeError):
                logger.warning(
                    f"Cannot parse segment_id '{segment_id}' as level number in event {event.id}"
                )
                return None
            return await self._resolution_service.resolve_segment_level_id_from_segment(
                event.sync_session_id, level_number
            )

        return None

    async def _create_progress(
        self, student_id: UUID, segment_level_id: UUID
    ) -> Progress:
        """
        Create a new progress record.

        Args:
            student_id: The student UUID
            segment_level_id: The segment level UUID

        Returns:
            Progress: The created progress record
        """
        data = {
            "student_id": student_id,
            "segment_level_id": segment_level_id,
            "attempt_count": 0,
            "error_count": 0,
            "hints_used_count": 0,
            "errors_details": None,
            "objectives_completed": 0,
            "efficiency_rating": 0,
        }
        return await self.repository.create(data)
