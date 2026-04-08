from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class CourseProfessor(Base):
    __tablename__ = "course_professors"

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    professor_id = Column(
        UUID(as_uuid=True), ForeignKey("professors.id"), nullable=False
    )

    course = relationship("Course", back_populates="course_professors")
    professor = relationship("Professor", back_populates="course_professors")
