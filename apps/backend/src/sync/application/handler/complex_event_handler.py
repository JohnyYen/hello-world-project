import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.infrastructure.mapper.sync_event_to_xapi_mapper import (
    SyncEventToXAPIMapper,
)
from src.statistic.application.service.xapi_statement_service import (
    XAPIStatementService,
)
from src.statistic.infrastructure.xapi_statement_repository import (
    XAPIStatementRepository,
)
from src.sync.application.handler.progress_updater import ProgressUpdater

logger = logging.getLogger(__name__)


class ComplexEventHandler:
    """
    Handler for complex sync events that require xAPI transformation.

    Complex events need to be mapped to xAPI statements, saved to the
    xAPI statements table, and then update the Progress table.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the complex event handler.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db
        self.mapper = SyncEventToXAPIMapper()
        self.xapi_repository = XAPIStatementRepository(db)
        self.xapi_service = XAPIStatementService(self.xapi_repository)
        self.progress_updater = ProgressUpdater(db)

    async def handle(self, event: SyncEvent) -> None:
        """
        Handle a complex sync event by mapping to xAPI, saving, then updating Progress.

        Args:
            event: The complex sync event to handle

        Raises:
            ValueError: If event type is not complex
        """
        from src.sync.domain.event_types import SyncEventType

        if not SyncEventType.is_complex(event.event_type):
            raise ValueError(
                f"Event type '{event.event_type}' is not a complex event type"
            )

        xapi_statement = await self.mapper.map(event)
        await self.xapi_service.save_statement(xapi_statement)

        await self.progress_updater.update(event)

        logger.info(f"Handled complex event {event.id} of type {event.event_type}")
