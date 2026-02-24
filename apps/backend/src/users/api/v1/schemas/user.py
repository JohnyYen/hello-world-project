import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from src.shared.api.schemas.base import ResponseSchema, DateTimeSchema

# ------------------------
# Funciones de validación compartidas
# ------------------------


def _validate_password_strength(v: str) -> str:
    """Valida que la contraseña cumpla con los requisitos de seguridad."""
    if len(v) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not re.search(r"[A-Z]", v):
        raise ValueError("La contraseña debe contener al menos una mayúscula")
    if not re.search(r"[a-z]", v):
        raise ValueError("La contraseña debe contener al menos una minúscula")
    if not re.search(r"\d", v):
        raise ValueError("La contraseña debe contener al menos un número")
    return v


# ------------------------
# Esquemas de Autenticación
# ------------------------


class UserLogin(BaseModel):
    """Esquema para inicio de sesión"""

    username: Optional[str] = Field(None, example="User")
    email: Optional[EmailStr] = Field(None, example="usuario@example.com")
    password: str = Field(..., min_length=8, example="Password123!")

    @model_validator(mode="before")
    def validate_credentials(cls, values):
        if not values.get("username") and not values.get("email"):
            raise ValueError("Debe proporcionar username o email")
        return values


class UserLoginResponse(BaseModel):
    """Respuesta de autenticación exitosa"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


# ------------------------
# Esquemas de Operaciones CRUD
# ------------------------


class UserBase(BaseModel):
    """Campos base compartidos"""

    username: str = Field(..., min_length=3, max_length=100, example="usuario")
    email: EmailStr = Field(..., example="usuario@example.com")


class UserCreate(UserBase):
    """
    Esquema para creación de usuario.

    Note: El role_id NO se incluye en el registro.
    El sistema asigna automáticamente el rol de 'professor' al usuario.
    """

    name: str = Field(..., min_length=1, max_length=255, example="John")
    lastname: Optional[str] = Field(None, max_length=255, example="Doe")
    password: str = Field(..., min_length=8, example="Password123!")

    @field_validator("password")
    def validate_password_strength(cls, v):
        return _validate_password_strength(v)


class UserUpdate(BaseModel):
    """Esquema para actualización de usuario"""

    email: Optional[EmailStr] = Field(None, example="nuevo@example.com")

    @field_validator("email")
    def email_not_empty(cls, v):
        if v == "":
            raise ValueError("El email no puede estar vacío")
        return v


class UserChangePassword(BaseModel):
    """Esquema para cambio de contraseña"""

    current_password: str = Field(..., example="Current123!")
    new_password: str = Field(..., min_length=8, example="NewPassword123!")

    @field_validator("new_password")
    def validate_new_password(cls, v):
        return _validate_password_strength(v)

    @model_validator(mode="before")
    def validate_password_change(cls, values):
        if values.get("current_password") == values.get("new_password"):
            raise ValueError("La nueva contraseña debe ser diferente a la actual")
        return values


# ------------------------
# Esquemas de Respuesta
# ------------------------


class UserRoleResponse(BaseModel):
    """Esquema para respuesta de rol"""

    id: int
    name: str = Field(..., alias="role_name")

    class Config:
        populate_by_name = True
        from_attributes = True


class UserResponse(UserBase, DateTimeSchema):
    """Esquema para respuesta de usuario"""

    id: int
    name: str
    lastname: Optional[str] = None
    is_active: bool = True
    role: Optional[UserRoleResponse] = None

    class Config:
        from_attributes = True


class UserListResponse(ResponseSchema):
    """Respuesta para listado de usuarios"""

    data: list[UserResponse] = []


class SingleUserResponse(ResponseSchema):
    """Respuesta para un solo usuario"""

    data: Optional[UserResponse] = None


# ------------------------
# Validaciones Adicionales
# ------------------------


def validate_email_allowed(email: str) -> str:
    """Valida dominios de email permitidos"""
    blocked_domains = ["example.com"]  # Dominios no permitidos
    domain = email.split("@")[-1]
    if domain in blocked_domains:
        raise ValueError(f"El dominio {domain} no está permitido")
    return email


# Actualizar referencias circulares
UserLoginResponse.model_rebuild()
