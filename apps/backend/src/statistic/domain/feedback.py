from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    comments = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="feedbacks")
