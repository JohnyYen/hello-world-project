from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LMSCredentialBase(BaseModel):
    """Base schema for LMS credentials."""

    user_id: int
    lms_url: str = Field(
        ..., description="URL del LMS (ej: https://moodle.university.edu)"
    )
    lms_email: str = Field(..., description="Email de la cuenta en el LMS")
    lms_password: str = Field(..., description="Contraseña de la cuenta LMS")
    lms_provider: str = Field(..., description="Proveedor LMS (moodle, canvas, etc.)")


class LMSCredentialCreate(LMSCredentialBase):
    """Schema for creating LMS credentials."""

    pass


class LMSCredentialUpdate(BaseModel):
    """Schema for updating LMS credentials."""

    lms_url: Optional[str] = None
    lms_email: Optional[str] = None
    lms_password: Optional[str] = None
    lms_provider: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expire_at: Optional[datetime] = None


class LMSCredentialResponse(BaseModel):
    """Schema for LMS credential response (password masked)."""

    id: int
    user_id: int
    lms_url: Optional[str] = None
    lms_email: str
    lms_provider: str
    access_token: Optional[str] = None
    expire_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LMSCredentialWithTokenResponse(LMSCredentialResponse):
    """Schema for LMS credential response including tokens (for internal use)."""

    lms_password: Optional[str] = None  # Normally masked, included for sync operations
    refresh_token: Optional[str] = None


class LMSCredentialDeleteResponse(BaseModel):
    """Schema for delete response."""

    message: str = "Credenciales LMS eliminadas correctamente"
    deleted_id: int
