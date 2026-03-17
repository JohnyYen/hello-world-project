import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.sync.domain.sync_event import SyncEvent
from src.sync.application.handler.progress_updater import ProgressUpdater

logger = logging.getLogger(__name__)


class SimpleEventHandler:
    """
    Handler for simple sync events that can be processed directly.

    Simple events are those that don't require xAPI transformation and
    can update the Progress table directly.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the simple event handler.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db
        self.progress_updater = ProgressUpdater(db)

    async def _get_student_id_from_event(self, event: SyncEvent) -> int | None:
        """Get student_id from sync_session -> game_instance chain."""
        # Get sync_session
        from src.sync.domain.sync_session import SyncSession

        result = await self.db.execute(
            select(SyncSession).where(SyncSession.id == event.sync_session_id)
        )
        sync_session = result.scalar_one_or_none()
        if not sync_session:
            return None

        # Get game_instance
        from src.game.domain.game_instance import GameInstance

        result = await self.db.execute(
            select(GameInstance).where(GameInstance.id == sync_session.instance_id)
        )
        game_instance = result.scalar_one_or_none()
        if not game_instance:
            return None

        return game_instance.student_id

    async def handle(self, event: SyncEvent) -> None:
        """
        Handle a simple sync event by directly updating Progress.

        Args:
            event The simple sync event to handle

        Raises:
            ValueError: If event type is not simple
        """
        from src.sync.domain.event_types import SyncEventType

        if not SyncEventType.is_simple(event.event_type):
            raise ValueError(
                f"Event type '{event.event_type}' is not a simple event type"
            )

        # Enrich payload with student_id if not present
        payload = event.payload or {}
        if "student_id" not in payload:
            student_id = await self._get_student_id_from_event(event)
            if student_id:
                payload["student_id"] = student_id
                event.payload = payload

        await self.progress_updater.update(event)
        logger.info(f"Handled simple event {event.id} of type {event.event_type}")
