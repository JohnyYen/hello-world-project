import logging
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.sync.domain.sync_event import SyncEvent
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress
from src.shared.domain.exceptions import NotFoundException
from src.game.domain.segment_level import SegmentLevel
from src.game.domain.level import Level

logger = logging.getLogger(__name__)


class ProgressUpdater:
    """
    Updates Progress records based on sync event types.

    Handles the logic for updating different progress metrics
    based on the event type.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the progress updater.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db
        self.repository = ProgressRepository(db)

    async def update(self, event: SyncEvent) -> None:
        """
        Update progress based on the event type.

        Args:
            event: The sync event to process
        """
        payload = event.payload or {}
        
        # Get student_id from sync_session chain or payload
        student_id = payload.get("student_id") or payload.get("actor_id")
        
        # Get segment_level_id - either directly or via game segment_id lookup
        segment_level_id = payload.get("segment_level_id")
        if not segment_level_id and "segment_id" in payload:
            segment_level_id = await self._resolve_segment_level_id(payload)

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

    async def _resolve_segment_level_id(self, payload: dict) -> str | None:
        """
        Resolve segment_id (from game) to segment_level UUID.
        
        Tries multiple strategies:
        1. segment_level_id already in payload
        2. Look up by game_id + segment position
        
        Args:
            payload: The event payload containing segment_id
            
        Returns:
            UUID string of segment_level, or None if not found
        """
        segment_id = payload.get("segment_id")
        game_id = payload.get("game_id")
        
        if not segment_id:
            return None
            
        # Strategy: Look up segment_level by position within the game
        # The game's segment_id corresponds to the position (1-indexed)
        result = await self.db.execute(
            select(SegmentLevel)
            .join(Level)
            .where(Level.game_id == game_id)
            .order_by(SegmentLevel.id)  # Assume ordered by creation
        )
        segments = result.scalars().all()
        
        # Try to match by position (segment_id is 1-indexed position)
        if segment_id <= len(segments):
            return str(segments[segment_id - 1].id)
            
        return None

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

        elif event_type == "raw_stats":
            # Bulk stats update - includes all metrics in one event
            update_data["attempt_count"] = payload.get("attempt_count", 0)
            update_data["error_count"] = payload.get("error_count", 0)
            update_data["hints_used_count"] = payload.get("hints_used_count", 0)
            update_data["errors_details"] = payload.get("errors_details")
            update_data["efficiency_rating"] = payload.get("efficiency_rating", 0)
            update_data["objectives_completed"] = payload.get("objectives_completed", 0)

        elif event_type == "level_time":
            pass

        elif event_type == "difficulty_changed":
            pass

        elif event_type == "adaptation":
            pass

        return update_data

    async def _create_progress(
        self, student_id: int, segment_level_id: int
    ) -> Progress:
        """
        Create a new progress record.

        Args:
            student_id: The student ID
            segment_level_id: The segment level ID

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
