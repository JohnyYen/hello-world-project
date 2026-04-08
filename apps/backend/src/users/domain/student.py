from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Student(Base):
    __tablename__ = "students"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="student")
    game_instances = relationship("GameInstance", back_populates="student")
    feedbacks = relationship("Feedback", back_populates="student")
    progresses = relationship("Progress", back_populates="student")
    xapi_statements = relationship("XAPIStatement", back_populates="student")
<<<<<<< HEAD
    course_enrollments = relationship("CourseEnrollment", back_populates="student")
=======
    enrollments = relationship("CourseEnrollment", back_populates="student")
>>>>>>> develop
