from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class SegmentLevel(Base):
    __tablename__ = "segment_levels"

    configuration = Column(JSON, nullable=True)
    level_number_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    # Relationships
    level = relationship("Level", back_populates="segments")
    progresses = relationship("Progress", back_populates="segment_level")
