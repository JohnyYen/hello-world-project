from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
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

    id: int
    username: str
    email: EmailStr
    name: str
    lastname: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
