from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    lms_id = Column(Integer, ForeignKey("lms_credentials.id"), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime, nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    role = relationship("Role", back_populates="users")
    lms_credential = relationship("LMSCredential", back_populates="user")
    student = relationship("Student", back_populates="user", uselist=False)
    professor = relationship("Professor", back_populates="user", uselist=False)
    teacher_settings = relationship("TeacherSettings", back_populates="user", uselist=False)
