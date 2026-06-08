from sqlalchemy import Boolean, Column, DateTime, Enum as SAEnum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.domain.enums import FeedbackType
from src.shared.infrastructure.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    comments = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    professor_id = Column(
        UUID(as_uuid=True), ForeignKey("professors.id"), nullable=False
    )
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=True)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=True)

    feedback_type = Column(
        SAEnum(FeedbackType, name="feedback_type_enum", create_constraint=True),
        nullable=False,
        default=FeedbackType.ADVICE,
    )
    display_in_game = Column(Boolean, nullable=False, default=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="feedbacks")
    professor = relationship("Professor", back_populates="feedbacks")
    game = relationship("Game", back_populates="feedbacks")
    level = relationship("Level", back_populates="feedbacks")
