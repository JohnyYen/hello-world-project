from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Course(Base):
    __tablename__ = "courses"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    enrollments = relationship("CourseEnrollment", back_populates="course")
    course_professors = relationship("CourseProfessor", back_populates="course")
