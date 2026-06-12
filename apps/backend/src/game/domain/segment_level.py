from sqlalchemy import Column, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class SegmentLevel(Base):
    __tablename__ = "segment_levels"

    __table_args__ = (
        UniqueConstraint("level_number_id", "segment_number", name="uq_segment_level_number"),
    )

    configuration = Column(JSON, nullable=True)
    level_number_id = Column(
        UUID(as_uuid=True), ForeignKey("levels.id"), nullable=False
    )
    segment_number = Column(Integer, nullable=False)

    # Relationships
    level = relationship("Level", back_populates="segments")
    progresses = relationship("Progress", back_populates="segment_level")
