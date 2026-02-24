from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.shared.api.schemas.base import ResponseSchema

# ------------------------
# Esquemas para Perfil de Profesor
# ------------------------


class TeacherProfileUpdate(BaseModel):
    """Esquema para actualización del perfil de profesor"""

    name: Optional[str] = Field(None, min_length=1, max_length=255, example="Juan")
    lastname: Optional[str] = Field(None, min_length=1, max_length=255, example="Pérez")
    email: Optional[EmailStr] = Field(None, example="nuevoemail@example.com")
    department: Optional[str] = Field(None, max_length=255, example="Matemáticas")
    contact_phone: Optional[str] = Field(None, max_length=20, example="+1234567890")
    avatar_url: Optional[str] = Field(None, example="https://example.com/avatar.jpg")


class TeacherProfileResponse(BaseModel):
    """Esquema para respuesta del perfil de profesor"""

    id: int
    username: str
    name: str
    lastname: str
    email: EmailStr
    department: str
    contact_phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ------------------------
# Esquemas para Configuraciones de Profesor
# ------------------------


class TeacherSettingsUpdate(BaseModel):
    """Esquema para actualización de configuraciones de profesor"""

    theme: Optional[str] = Field(
        None, example="dark", description="Tema de la interfaz: light o dark"
    )
    notifications_enabled: Optional[bool] = Field(
        None, example=True, description="Habilitar notificaciones"
    )
    notification_frequency: Optional[str] = Field(
        None,
        example="instant",
        description="Frecuencia de notificaciones: instant, daily, weekly",
    )
    interface_language: Optional[str] = Field(
        None, example="es", description="Idioma de la interfaz"
    )


class TeacherSettingsResponse(BaseModel):
    """Esquema para respuesta de configuraciones de profesor"""

    theme: str = "light"
    notifications_enabled: bool = True
    notification_frequency: str = "instant"
    interface_language: str = "es"

    class Config:
        from_attributes = True


# ------------------------
# Esquemas de Respuesta
# ------------------------


class TeacherProfileResponseSchema(ResponseSchema):
    """Respuesta para el perfil de profesor"""

    data: TeacherProfileResponse


class TeacherSettingsResponseSchema(ResponseSchema):
    """Respuesta para las configuraciones de profesor"""

    data: TeacherSettingsResponse


class TeacherUpdateResponseSchema(ResponseSchema):
    """Respuesta para actualizaciones de profesor"""

    message: str = "Perfil actualizado exitosamente"
    data: TeacherProfileResponse
