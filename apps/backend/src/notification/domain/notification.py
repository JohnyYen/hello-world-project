from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    notification_type = Column(String(50), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        Index("ix_notifications_entity_type_entity_id", "entity_type", "entity_id"),
    )

    user = relationship("User", back_populates="notifications")
