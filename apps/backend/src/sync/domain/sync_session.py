from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class SyncSession(Base):
    __tablename__ = "sync_sessions"

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(255), nullable=True)

    instance_id = Column(
        UUID(as_uuid=True), ForeignKey("game_instances.id"), nullable=False
    )

    # Relationships using string references to avoid circular imports
    game_instance = relationship(
        "src.game.domain.game_instance.GameInstance", back_populates="sync_sessions"
    )
    events = relationship(
        "src.sync.domain.sync_event.SyncEvent", back_populates="sync_session"
    )
