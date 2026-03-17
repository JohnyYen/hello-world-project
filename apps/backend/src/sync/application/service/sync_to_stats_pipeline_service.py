from typing import List, Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.event_types import SyncEventType
from src.sync.application.handler.simple_event_handler import SimpleEventHandler
from src.sync.application.handler.complex_event_handler import ComplexEventHandler
from src.sync.application.handler.dead_letter_handler import DeadLetterHandler

logger = logging.getLogger(__name__)


class SyncToStatsPipelineService:
    """
    Pipeline service that processes sync events and forwards them to the statistics system.

    This service acts as a router, classifying events as simple or complex
    and delegating to the appropriate handler.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the pipeline service.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db
        self.simple_handler = SimpleEventHandler(db)
        self.complex_handler = ComplexEventHandler(db)
        self.dead_letter_handler = DeadLetterHandler(db)

    async def process_event(self, event: SyncEvent) -> bool:
        """
        Process a single sync event, routing to the appropriate handler.

        Args:
            event: The sync event to process

        Returns:
            bool: True if processing succeeded, False otherwise
        """
        try:
            event_type = event.event_type

            if not self._is_valid_event_type(event_type):
                logger.warning(
                    f"Invalid event type '{event_type}' for event {event.id}"
                )
                await self.dead_letter_handler.handle(
                    event, f"Unknown event type: {event_type}"
                )
                return False

            classification = SyncEventType.classify(event_type)

            if classification == SyncEventType.SIMPLE:
                await self.simple_handler.handle(event)
            else:
                await self.complex_handler.handle(event)

            await self._update_event_status(event, "processed")
            logger.info(f"Successfully processed event {event.id} of type {event_type}")
            return True

        except Exception as e:
            logger.error(f"Error processing event {event.id}: {str(e)}")
            await self.dead_letter_handler.handle(event, str(e))
            await self._update_event_status(event, "failed")
            return False

    async def process_batch(self, events: List[SyncEvent]) -> dict:
        """
        Process multiple sync events in batch.

        Args:
            events: List of sync events to process

        Returns:
            dict: Summary with success and failure counts
        """
        results = {
            "total": len(events),
            "successful": 0,
            "failed": 0,
        }

        for event in events:
            success = await self.process_event(event)
            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1

        logger.info(
            f"Batch processing complete: {results['successful']}/{results['total']} succeeded"
        )
        return results

    def _is_valid_event_type(self, event_type: str) -> bool:
        """
        Check if the event type is valid.

        Args:
            event_type: The event type to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            SyncEventType.classify(event_type)
            return True
        except ValueError:
            return False

    async def _update_event_status(self, event: SyncEvent, status: str) -> None:
        """
        Update the status of a sync event.

        Args:
            event: The event to update
            status: The new status
        """
        event.status = status
        await self.db.commit()
