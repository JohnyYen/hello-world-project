from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID
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

    id: str | UUID
    username: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: EmailStr
    department: Optional[str] = None
    contact_phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True


# ------------------------
# Esquemas para Configuraciones de Profesor
# ------------------------


class TeacherSettingsUpdate(BaseModel):
    """Esquema para actualización de configuraciones de profesor"""

    # Original fields
    theme: Optional[Literal["light", "dark"]] = Field(
        None, example="dark", description="Tema de la interfaz: light o dark"
    )
    notifications_enabled: Optional[bool] = Field(
        None, example=True, description="Habilitar notificaciones"
    )
    notification_frequency: Optional[
        Literal["realtime", "daily", "weekly", "disabled"]
    ] = Field(
        None,
        example="realtime",
        description="Frecuencia de notificaciones: realtime, daily, weekly, disabled",
    )
    interface_language: Optional[Literal["es", "en"]] = Field(
        None, example="es", description="Idioma de la interfaz"
    )
    # Session settings
    auto_logout: Optional[bool] = Field(
        None, example=False, description="Cerrar sesión automáticamente por inactividad"
    )
    session_duration_minutes: Optional[int] = Field(
        None,
        ge=0,
        example=60,
        description="Duración de la sesión en minutos (0 = permanente)",
    )
    remember_login: Optional[bool] = Field(
        None, example=True, description="Recordar inicio de sesión en este dispositivo"
    )
    # Appearance settings
    color_theme: Optional[
        Literal["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"]
    ] = Field(
        None,
        example="Indigo",
        description="Tema de color: Indigo, Violeta, Esmeralda, Azul, Rosa, Naranja",
    )
    animations_enabled: Optional[bool] = Field(
        None, example=True, description="Habilitar animaciones y transiciones"
    )
    # Notification settings (extended)
    email_notifications: Optional[bool] = Field(
        None, example=False, description="Recibir notificaciones por email"
    )
    # Language settings (extended)
    date_format: Optional[Literal["ddmmyyyy", "mmddyyyy", "yyyymmdd"]] = Field(
        None,
        example="ddmmyyyy",
        description="Formato de fecha: ddmmyyyy, mmddyyyy, yyyymmdd",
    )
    timezone: Optional[Literal["gmt-5", "gmt-6", "gmt-3", "gmt0", "gmt1"]] = Field(
        None,
        example="gmt-5",
        description="Zona horaria: gmt-5, gmt-6, gmt-3, gmt0, gmt1",
    )


class TeacherSettingsResponse(BaseModel):
    """Esquema para respuesta de configuraciones de profesor"""

    # Original fields
    theme: Literal["light", "dark"] = "light"
    notifications_enabled: bool = True
    notification_frequency: Literal["realtime", "daily", "weekly", "disabled"] = (
        "realtime"
    )
    interface_language: Literal["es", "en"] = "es"
    # Session settings
    auto_logout: Optional[bool] = None
    session_duration_minutes: Optional[int] = None
    remember_login: Optional[bool] = None
    # Appearance settings
    color_theme: Optional[
        Literal["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"]
    ] = None
    animations_enabled: Optional[bool] = None
    # Notification settings (extended)
    email_notifications: Optional[bool] = None
    # Language settings (extended)
    date_format: Optional[Literal["ddmmyyyy", "mmddyyyy", "yyyymmdd"]] = None
    timezone: Optional[Literal["gmt-5", "gmt-6", "gmt-3", "gmt0", "gmt1"]] = None

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
