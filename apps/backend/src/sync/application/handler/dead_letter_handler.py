import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.sync_event_failure import SyncEventFailure
from src.shared.infrastructure.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class DeadLetterHandler:
    """
    Handler for failed sync events.

    Stores failed events in a dead letter table for manual review
    and potential reprocessing.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the dead letter handler.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db
        self.repository = BaseRepository(db, SyncEventFailure)

    async def handle(self, event: SyncEvent, error_message: str) -> None:
        """
        Store a failed event in the dead letter table.

        Args:
            event: The failed sync event
            error_message: The error message from the failure
        """
        failure_data = {
            "original_event_id": event.id,
            "event_type": event.event_type,
            "payload": event.payload,
            "sync_session_id": event.sync_session_id,
            "timestamp": event.timestamp,
            "error_message": error_message,
            "failed_at": datetime.now(timezone.utc),
            "retry_count": 0,
            "status": "pending",
        }

        await self.repository.create(failure_data)
        await self.db.commit()

        logger.warning(f"Event {event.id} moved to dead letter. Error: {error_message}")

    async def get_pending_failures(self, limit: int = 100) -> list[SyncEventFailure]:
        """
        Get pending failures for manual review.

        Args:
            limit: Maximum number of failures to retrieve

        Returns:
            list[SyncEventFailure]: List of pending failures
        """
        filters = {"status": "pending"}
        return await self.repository.get_by_filters(filters, limit=limit)

    async def mark_retry(self, failure_id: int) -> None:
        """
        Increment retry count for a failure.

        Args:
            failure_id: The ID of the failure record
        """
        failure = await self.repository.get_by_id(failure_id)
        if failure:
            failure.retry_count += 1
            await self.db.commit()

    async def mark_resolved(self, failure_id: int) -> None:
        """
        Mark a failure as resolved.

        Args:
            failure_id: The ID of the failure record
        """
        failure = await self.repository.get_by_id(failure_id)
        if failure:
            failure.status = "resolved"
            await self.db.commit()
