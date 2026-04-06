from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class LMSCredential(Base):
    """
    Modelo de credenciales LMS para integración con plataformas externas.

    Almacena las credenciales necesarias para conectarse a sistemas LMS
    como Moodle, Canvas, etc.
    """

    __tablename__ = "lms_credentials"

    lms_email = Column(String(255), unique=True, nullable=False)
    lms_password = Column(String(255), nullable=False)
    lms_provider = Column(String(255), nullable=False)
    lms_url = Column(String(500), nullable=True)
    access_token = Column(String(500), nullable=True)
    refresh_token = Column(String(500), nullable=True)
    expire_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship with User
    user = relationship("User", back_populates="lms_credential", uselist=False)
