from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID


# ------------------------
# Esquemas Base
# ------------------------


class GameBase(BaseModel):
    """Campos base compartidos para Game"""

    title: str = Field(
        ..., min_length=1, max_length=255, example="Juego de Matemáticas"
    )
    description: Optional[str] = Field(
        None, max_length=255, example="Aprende matemáticas básicas"
    )
    creator: Optional[str] = Field(None, max_length=255, example="Profesor García")
    subject: Optional[str] = Field(None, max_length=255, example="Matemáticas")
    download_link: str = Field(
        ..., min_length=1, max_length=500, example="https://games.helloworld.edu/math-game.zip"
    )


# ------------------------
# Esquemas de Request
# ------------------------


class GameCreate(GameBase):
    """Esquema para creación de juego"""

    pass


class GameUpdate(BaseModel):
    """Esquema para actualización de juego"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, example="Juego de Matemáticas"
    )
    description: Optional[str] = Field(
        None, max_length=255, example="Aprende matemáticas básicas"
    )
    creator: Optional[str] = Field(None, max_length=255, example="Profesor García")
    subject: Optional[str] = Field(None, max_length=255, example="Matemáticas")
    download_link: Optional[str] = Field(
        None, max_length=500, example="https://games.helloworld.edu/math-game.zip"
    )


# ------------------------
# Esquemas de Respuesta
# ------------------------


class GameResponse(GameBase):
    """Esquema para respuesta de juego"""

    model_config = ConfigDict(from_attributes=True)

    id: str | UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class GameDetailResponse(GameResponse):
    """Esquema para respuesta detallada de juego con relaciones"""

    levels_count: int = Field(0, description="Cantidad de niveles del juego")


class GameListResponse(BaseModel):
    """Esquema para listado de juegos"""

    success: bool = True
    message: str = "Juegos obtenidos exitosamente"
    data: List[GameResponse] = []
    total: int = 0
    skip: int = 0
    limit: int = 10


class SingleGameResponse(BaseModel):
    """Esquema para respuesta de un solo juego"""

    success: bool = True
    message: str = "Juego obtenido exitosamente"
    data: Optional[GameDetailResponse] = None


class GameCreateResponse(BaseModel):
    """Esquema para respuesta de creación de juego"""

    success: bool = True
    message: str = "Juego creado exitosamente"
    data: GameResponse


class GameUpdateResponse(BaseModel):
    """Esquema para respuesta de actualización de juego"""

    success: bool = True
    message: str = "Juego actualizado exitosamente"
    data: GameResponse


class GameDeleteResponse(BaseModel):
    """Esquema para respuesta de eliminación de juego"""

    success: bool = True
    message: str = "Juego eliminado exitosamente"
