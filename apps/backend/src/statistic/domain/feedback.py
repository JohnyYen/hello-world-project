from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    comments = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    professor_id = Column(
        UUID(as_uuid=True), ForeignKey("professors.id"), nullable=False
    )
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="feedbacks")
    professor = relationship("Professor", back_populates="feedbacks")
    game = relationship("Game", back_populates="feedbacks")
    level = relationship("Level", back_populates="feedbacks")
