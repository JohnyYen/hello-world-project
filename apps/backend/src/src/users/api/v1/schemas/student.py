from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from src.shared.api.schemas.base import ResponseSchema


class StudentCreate(BaseModel):
    """Esquema para crear un nuevo estudiante"""

    username: str
    email: EmailStr
    name: str
    lastname: str
    password: str
    is_active: Optional[bool] = True


class StudentUpdate(BaseModel):
    """Esquema para actualizar la información del estudiante"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponse(BaseModel):
    """Esquema para la respuesta individual del estudiante"""

    id: UUID
    username: str
    email: EmailStr
    name: str
    lastname: str
    is_active: bool
    course: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Activity tracking fields
    last_active_at: Optional[datetime] = None
    current_streak_days: bool = False
    active_today: bool = False

    class Config:
        from_attributes = True


class StudentListResponse(ResponseSchema):
    """Esquema para la respuesta de listado de estudiantes"""

    data: List[StudentResponse]


class StudentProgressResponse(ResponseSchema):
    """Esquema para la respuesta de progreso del estudiante"""

    data: dict


class StudentReportsResponse(ResponseSchema):
    """Esquema para la respuesta de reportes del estudiante"""

    data: dict
