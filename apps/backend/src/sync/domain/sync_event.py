from sqlalchemy import Column, String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class SyncEvent(Base):
    __tablename__ = "sync_events"

    event_type = Column(String(255), nullable=False)
    payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=True)

    sync_session_id = Column(Integer, ForeignKey("sync_sessions.id"), nullable=False)

    # Relationships using string references to avoid circular imports
    sync_session = relationship(
        "src.sync.domain.sync_session.SyncSession", back_populates="events"
    )
