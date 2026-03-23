from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Progress(Base):
    __tablename__ = "progresses"

    attempt_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    hints_used_count = Column(Integer, default=0, nullable=False)
    errors_details = Column(JSON, nullable=True)
    objectives_completed = Column(Integer, default=0, nullable=False)
    efficiency_rating = Column(Integer, default=0, nullable=False)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    segment_level_id = Column(
        UUID(as_uuid=True), ForeignKey("segment_levels.id"), nullable=False
    )

    # Relationships
    student = relationship("Student", back_populates="progresses")
    segment_level = relationship("SegmentLevel", back_populates="progresses")
