<<<<<<< HEAD
from sqlalchemy import Column, String, Text, Boolean, Date
=======
from sqlalchemy import Column, String, Text, Boolean
>>>>>>> develop
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Course(Base):
    __tablename__ = "courses"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
<<<<<<< HEAD
    school_year = Column(String(20), nullable=False)
    period_label = Column(String(50), nullable=False)
    display_period = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    enrollments = relationship("CourseEnrollment", back_populates="course")

    def __repr__(self) -> str:
        return f"<Course(id={self.id}, name={self.name}, period={self.display_period})>"
=======
    is_active = Column(Boolean, default=True, nullable=False)

    enrollments = relationship("CourseEnrollment", back_populates="course")
    course_professors = relationship("CourseProfessor", back_populates="course")
>>>>>>> develop
