import logging
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.sync_session import SyncSession
from src.game.domain.game_instance import GameInstance
from src.game.domain.level import Level
from src.game.domain.segment_level import SegmentLevel
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

        # Fall back to actor_id when student_id is not present
        # (xapi_statement events from the game send actor_id)
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

    async def _resolve_segment_level_id(self, event: SyncEvent) -> Optional[UUID]:
        """
        Resolve segment_level_id from the sync session chain.

        For xapi_statement events, the payload contains object_id (level number)
        and object_type instead of a direct segment_level_id. This method
        traverses: SyncEvent → SyncSession → GameInstance → Level → SegmentLevel

        Args:
            event: The sync event to resolve segment_level_id for

        Returns:
            UUID of the SegmentLevel, or None if it cannot be resolved
        """
        payload = event.payload or {}
        object_type = payload.get("object_type")
        object_id = payload.get("object_id")

        # Only resolve for level-type objects
        if object_type != "level" or not object_id:
            return None

        try:
            level_number = int(object_id)
        except (ValueError, TypeError):
            logger.warning(
                f"Cannot parse object_id '{object_id}' as level number in event {event.id}"
            )
            return None

        # 1. Get SyncSession
        session_result = await self.db.execute(
            select(SyncSession).where(
                SyncSession.id == event.sync_session_id,
                SyncSession.deleted_at.is_(None),
            )
        )
        sync_session = session_result.scalar_one_or_none()
        if not sync_session:
            logger.warning(f"SyncSession {event.sync_session_id} not found for event {event.id}")
            return None

        # 2. Get GameInstance (which has student_id and game_id)
        instance_result = await self.db.execute(
            select(GameInstance).where(
                GameInstance.id == sync_session.instance_id,
                GameInstance.deleted_at.is_(None),
            )
        )
        game_instance = instance_result.scalar_one_or_none()
        if not game_instance:
            logger.warning(
                f"GameInstance {sync_session.instance_id} not found for sync session {sync_session.id}"
            )
            return None

        # 3. Find Level by game_id and level_number
        level_result = await self.db.execute(
            select(Level).where(
                Level.game_id == game_instance.game_id,
                Level.level_number == level_number,
                Level.deleted_at.is_(None),
            )
        )
        level = level_result.scalar_one_or_none()
        if not level:
            logger.warning(
                f"Level not found for game {game_instance.game_id}, number {level_number}"
            )
            return None

        # 4. Find the first SegmentLevel for this Level
        # (a Level can have multiple SegmentLevels; use the first one)
        segment_result = await self.db.execute(
            select(SegmentLevel)
            .where(
                SegmentLevel.level_number_id == level.id,
                SegmentLevel.deleted_at.is_(None),
            )
            .limit(1)
        )
        segment_level = segment_result.scalar_one_or_none()
        if not segment_level:
            logger.warning(f"No SegmentLevel found for level {level.id}")
            return None

        logger.info(
            f"Resolved segment_level_id={segment_level.id} from "
            f"level_number={level_number}, game={game_instance.game_id}"
        )
        return segment_level.id

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

        elif event_type == "level_time":
            pass

        elif event_type == "difficulty_changed":
            pass

        elif event_type == "adaptation":
            pass

        return update_data

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
