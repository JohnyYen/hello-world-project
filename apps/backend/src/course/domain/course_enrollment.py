from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.shared.infrastructure.base import Base


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    enrolled_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")
