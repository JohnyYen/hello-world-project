from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Professor(Base):
    __tablename__ = "professors"

    department = Column(String(255), nullable=False)
    contact_phone = Column(String(255), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="professor")
    feedbacks = relationship("Feedback", back_populates="professor")
    course_professors = relationship("CourseProfessor", back_populates="professor")
