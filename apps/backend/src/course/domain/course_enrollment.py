<<<<<<< HEAD
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
=======
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
>>>>>>> develop
from src.shared.infrastructure.base import Base


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

<<<<<<< HEAD
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="course_enrollments")

    def __repr__(self) -> str:
        return f"<CourseEnrollment(course_id={self.course_id}, student_id={self.student_id})>"
=======
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    enrolled_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")
>>>>>>> develop
