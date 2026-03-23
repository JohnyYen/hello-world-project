from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class TeacherSettings(Base):
    __tablename__ = "teacher_settings"

    theme = Column(String(50), default="light", nullable=False)  # light or dark
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    notification_frequency = Column(
        String(50), default="realtime", nullable=False
    )  # realtime, daily, weekly, disabled
    interface_language = Column(
        String(10), default="es", nullable=False
    )  # es, en, etc.

    # Session settings
    auto_logout = Column(Boolean, nullable=True)
    session_duration_minutes = Column(Integer, nullable=True)
    remember_login = Column(Boolean, nullable=True)

    # Appearance settings
    color_theme = Column(String(50), nullable=True)
    animations_enabled = Column(Boolean, nullable=True)

    # Notification settings (extended)
    email_notifications = Column(Boolean, nullable=True)

    # Language settings (extended)
    date_format = Column(String(20), nullable=True)
    timezone = Column(String(50), nullable=True)

    # Foreign key to connect with user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="teacher_settings")
