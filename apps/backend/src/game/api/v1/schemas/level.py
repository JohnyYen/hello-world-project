from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID


# ------------------------
# Esquemas Base
# ------------------------


class LevelBase(BaseModel):
    """Campos base compartidos para Level"""

    level_number: int
    title: str
    description: Optional[str] = None
    goal: Optional[str] = None


# ------------------------
# Esquemas de Request
# ------------------------


class LevelCreate(LevelBase):
    """Esquema para creación de nivel"""

    game_id: Optional[int] = None


class LevelUpdate(BaseModel):
    """Esquema para actualización de nivel"""

    level_number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None


# ------------------------
# Esquemas de Respuesta
# ------------------------


class LevelResponse(LevelBase):
    """Esquema para respuesta de nivel"""

    model_config = ConfigDict(from_attributes=True)

    id: str | UUID
    game_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class LevelDetailResponse(LevelResponse):
    """Esquema para respuesta detallada de nivel con segmentos"""

    segments_count: int = 0


class LevelListResponse(BaseModel):
    """Esquema para listado de niveles"""

    success: bool = True
    message: str = "Niveles obtenidos exitosamente"
    data: List[LevelResponse] = []
    total: int = 0


class SingleLevelResponse(BaseModel):
    """Esquema para respuesta de un solo nivel"""

    success: bool = True
    message: str = "Nivel obtenido exitosamente"
    data: Optional[LevelDetailResponse] = None


class LevelCreateResponse(BaseModel):
    """Esquema para respuesta de creación de nivel"""

    success: bool = True
    message: str = "Nivel creado exitosamente"
    data: LevelResponse


class LevelUpdateResponse(BaseModel):
    """Esquema para respuesta de actualización de nivel"""

    success: bool = True
    message: str = "Nivel actualizado exitosamente"
    data: LevelResponse


class LevelDeleteResponse(BaseModel):
    """Esquema para respuesta de eliminación de nivel"""

    success: bool = True
    message: str = "Nivel eliminado exitosamente"
