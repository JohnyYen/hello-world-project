import logging
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def handle(self, event: SyncEvent) -> None:
        """
        Handle a simple sync event by directly updating Progress.

        Args:
            event: The simple sync event to handle

        Raises:
            ValueError: If event type is not simple
        """
        from src.sync.domain.event_types import SyncEventType

        if not SyncEventType.is_simple(event.event_type):
            raise ValueError(
                f"Event type '{event.event_type}' is not a simple event type"
            )

        await self.progress_updater.update(event)
        logger.info(f"Handled simple event {event.id} of type {event.event_type}")
