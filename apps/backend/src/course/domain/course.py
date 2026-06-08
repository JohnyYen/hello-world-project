from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Course(Base):
    __tablename__ = "courses"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    school_year = Column(String(20), nullable=False)  # Ej: "2025-2026"
    period_label = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)

    # Relationships
    enrollments = relationship("CourseEnrollment", back_populates="course")
    course_professors = relationship("CourseProfessor", back_populates="course")
    game = relationship("Game", back_populates="courses")

    def __repr__(self) -> str:
        return f"<Course(id={self.id}, name={self.name}, school_year={self.school_year})>"
