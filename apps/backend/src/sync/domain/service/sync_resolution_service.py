import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_session import SyncSession
from src.game.domain.game_instance import GameInstance
from src.game.domain.level import Level
from src.game.domain.segment_level import SegmentLevel


logger = logging.getLogger(__name__)


class SyncResolutionService:
    """
    Resolves entity IDs through the sync session chain.

    Chain: SyncSession -> GameInstance -> Level -> SegmentLevel

    This centralizes the chain traversal logic that was previously
    duplicated in ProgressUpdater and SimpleEventHandler.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def resolve_student_id(self, sync_session_id: UUID) -> Optional[UUID]:
        """
        Resolve student_id from the sync session chain.

        Traverses: SyncSession -> GameInstance -> student_id

        Args:
            sync_session_id: UUID of the SyncSession

        Returns:
            UUID of the Student, or None if it cannot be resolved
        """
        sync_session = await self._get_sync_session(sync_session_id)
        if not sync_session:
            return None

        game_instance = await self._get_game_instance(sync_session.instance_id)
        if not game_instance:
            return None

        logger.info(
            f"Resolved student_id={game_instance.student_id} from "
            f"game_instance {game_instance.id}"
        )
        return game_instance.student_id

    async def resolve_segment_level_id_from_object(
        self,
        sync_session_id: UUID,
        level_number: int,
        segment_number: Optional[int] = None,
    ) -> Optional[UUID]:
        """
        Resolve segment_level_id from the sync session chain using a level number
        and optionally a segment number.

        Traverses: SyncSession -> GameInstance -> Level -> SegmentLevel

        Args:
            sync_session_id: UUID of the SyncSession
            level_number: The level number to look up
            segment_number: Optional segment number. When None (legacy format),
                falls back to .limit(1) in the segment query.

        Returns:
            UUID of the SegmentLevel, or None if it cannot be resolved
        """
        sync_session = await self._get_sync_session(sync_session_id)
        if not sync_session:
            return None

        game_instance = await self._get_game_instance(sync_session.instance_id)
        if not game_instance:
            return None

        level = await self._get_level(game_instance.game_id, level_number)
        if not level:
            return None

        segment_level = await self._get_segment_level(level.id, segment_number)
        if not segment_level:
            return None

        logger.info(
            f"Resolved segment_level_id={segment_level.id} from "
            f"level_number={level_number}, segment_number={segment_number}, "
            f"game={game_instance.game_id}"
        )
        return segment_level.id

    async def resolve_segment_level_id_from_segment(
        self, sync_session_id: UUID, segment_id: int
    ) -> Optional[UUID]:
        """
        Resolve segment_level_id from the sync session chain using a segment_id.

        Same chain as resolve_segment_level_id_from_object but uses segment_id
        (which maps to Level.level_number) instead of level_number directly.

        Traverses: SyncSession -> GameInstance -> Level -> SegmentLevel

        Args:
            sync_session_id: UUID of the SyncSession
            segment_id: The segment ID (maps to Level.level_number)

        Returns:
            UUID of the SegmentLevel, or None if it cannot be resolved
        """
        return await self.resolve_segment_level_id_from_object(
            sync_session_id, segment_id
        )

    async def _get_sync_session(self, sync_session_id: UUID) -> Optional[SyncSession]:
        result = await self.db.execute(
            select(SyncSession).where(
                SyncSession.id == sync_session_id,
                SyncSession.deleted_at.is_(None),
            )
        )
        sync_session = result.scalar_one_or_none()
        if not sync_session:
            logger.warning(f"SyncSession {sync_session_id} not found")
            return None
        return sync_session

    async def _get_game_instance(
        self, instance_id: UUID
    ) -> Optional[GameInstance]:
        result = await self.db.execute(
            select(GameInstance).where(
                GameInstance.id == instance_id,
                GameInstance.deleted_at.is_(None),
            )
        )
        game_instance = result.scalar_one_or_none()
        if not game_instance:
            logger.warning(f"GameInstance {instance_id} not found")
            return None
        return game_instance

    async def _get_level(
        self, game_id: UUID, level_number: int
    ) -> Optional[Level]:
        result = await self.db.execute(
            select(Level).where(
                Level.game_id == game_id,
                Level.level_number == level_number,
                Level.deleted_at.is_(None),
            )
        )
        level = result.scalar_one_or_none()
        if not level:
            logger.warning(
                f"Level not found for game {game_id}, number {level_number}"
            )
            return None
        return level

    async def _get_segment_level(
        self, level_id: UUID, segment_number: Optional[int] = None
    ) -> Optional[SegmentLevel]:
        query = select(SegmentLevel).where(
            SegmentLevel.level_number_id == level_id,
            SegmentLevel.deleted_at.is_(None),
        )

        if segment_number is not None:
            query = query.where(SegmentLevel.segment_number == segment_number)
        else:
            query = query.limit(1)

        result = await self.db.execute(query)
        segment_level = result.scalar_one_or_none()
        if not segment_level:
            if segment_number is not None:
                logger.warning(
                    f"No SegmentLevel found for level {level_id}, segment {segment_number}"
                )
            else:
                logger.warning(f"No SegmentLevel found for level {level_id}")
            return None
        return segment_level
