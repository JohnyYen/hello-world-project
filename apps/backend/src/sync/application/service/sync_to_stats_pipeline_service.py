from typing import List, Optional
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.event_types import SyncEventType
from src.sync.application.handler.simple_event_handler import SimpleEventHandler
from src.sync.application.handler.complex_event_handler import ComplexEventHandler
from src.sync.application.handler.dead_letter_handler import DeadLetterHandler
from src.shared.infrastructure.session import SessionLocal

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

    async def process_event(self, event: SyncEvent | int) -> bool:
        """
        Process a single sync event, routing to the appropriate handler.

        Args:
            event: The sync event to process or its ID

        Returns:
            bool: True if processing succeeded, False otherwise
        """
        from src.sync.infrastructure.repositories.sync_event_repository import (
            SyncEventRepository,
        )

        try:
            # If event is an ID, reload it in current session
            if isinstance(event, int):
                repository = SyncEventRepository(self.db)
                event = await repository.get_by_id(event)
                if not event:
                    logger.warning(f"Event {event} not found for processing")
                    return False

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
            logger.error(f"Error processing event: {str(e)}")
            if isinstance(event, SyncEvent):
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


# Module-level function for background processing
async def _process_event_pipeline(event_id: int) -> None:
    """
    Background task to process sync events through the stats pipeline.

    This function runs in the background to avoid blocking the main request.
    It handles retries with exponential backoff.

    Args:
        event_id: ID of the event to process
    """
    from src.sync.infrastructure.repositories.sync_event_repository import (
        SyncEventRepository,
    )

    max_attempts = 3
    base_delay = 1.0

    for attempt in range(1, max_attempts + 1):
        try:
            async with SessionLocal() as db:
                repository = SyncEventRepository(db)
                pipeline = SyncToStatsPipelineService(db)

                # Reload event in new session to ensure clean state
                event = await repository.get_by_id(event_id)

                if not event:
                    logger.warning(
                        f"Event {event_id} not found for pipeline processing"
                    )
                    return

                await pipeline.process_event(event)
                logger.info(f"Pipeline processing completed for event {event_id}")
                return

        except Exception as e:
            logger.warning(
                f"Pipeline attempt {attempt}/{max_attempts} failed for event {event_id}: {str(e)}"
            )

            if attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"Pipeline failed after {max_attempts} attempts for event {event_id}. "
                    f"Sending to dead letter."
                )
                await _send_event_to_dead_letter(event_id, str(e))


async def _send_event_to_dead_letter(event_id: int, error_message: str) -> None:
    """
    Send a failed event to the dead letter handler.

    Args:
        event_id: ID of the failed event
        error_message: Error message from the failure
    """
    from src.sync.infrastructure.repositories.sync_event_repository import (
        SyncEventRepository,
    )

    try:
        async with SessionLocal() as db:
            repository = SyncEventRepository(db)
            dead_letter_handler = DeadLetterHandler(db)

            event = await repository.get_by_id(event_id)
            if event:
                await dead_letter_handler.handle(event, error_message)
                logger.info(f"Event {event_id} sent to dead letter")
    except Exception as e:
        logger.error(f"Failed to send event {event_id} to dead letter: {str(e)}")
