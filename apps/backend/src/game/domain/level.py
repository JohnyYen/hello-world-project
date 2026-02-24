from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Level(Base):
    __tablename__ = "levels"

    level_number = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    goal = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

    # Relationships
    game = relationship("Game", back_populates="levels")
    segments = relationship("SegmentLevel", back_populates="level")
