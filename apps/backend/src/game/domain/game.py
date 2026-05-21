from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Game(Base):
    __tablename__ = "games"

    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    creator = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)
    publication_status = Column(String(255), nullable=True)

    # Relationships
    levels = relationship("Level", back_populates="game")
    instances = relationship("GameInstance", back_populates="game")
    feedbacks = relationship("Feedback", back_populates="game")
    courses = relationship("Course", back_populates="game")
