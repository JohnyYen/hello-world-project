from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class StudentActivityLog(Base):
    __tablename__ = "student_activity_log"

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    # Use 'metadata' for database column but 'extra_data' as attribute name
    extra_data = Column("metadata", JSONB, default={})

    student = relationship("User", back_populates="activity_logs")