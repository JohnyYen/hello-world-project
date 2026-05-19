from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, Text, JSON
from src.shared.infrastructure.base import Base


class SyncEventFailure(Base):
    """
    Model for storing failed sync events for manual review.

    When an event fails processing, it's stored here along with
    the error details for later investigation.
    """

    __tablename__ = "sync_event_failures"

    original_event_id = Column(Integer, nullable=True)
    event_type = Column(String(255), nullable=False)
    payload = Column(JSON, nullable=True)
    sync_session_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    error_message = Column(Text, nullable=False)
    failed_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    retry_count = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="pending", nullable=False)
