from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class TeacherSettings(Base):
    __tablename__ = "teacher_settings"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String(50), default="light", nullable=False)  # light or dark
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    notification_frequency = Column(String(50), default="instant", nullable=False)  # instant, daily, weekly
    interface_language = Column(String(10), default="es", nullable=False)  # es, en, etc.
    
    # Foreign key to connect with user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="teacher_settings")