from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ------------------------
# Esquemas de Request
# ------------------------


class GameInstanceCreate(BaseModel):
    """Esquema para crear una nueva instancia de juego"""

    game_id: Optional[int] = None
    student_id: int
    status: Optional[str] = "active"  # active, completed, abandoned


class GameInstanceUpdate(BaseModel):
    """Esquema para actualizar una instancia de juego"""

    status: Optional[str] = None


class GameInstanceEnd(BaseModel):
    """Esquema para finalizar una instancia de juego"""

    status: str = "completed"  # completed, abandoned


# ------------------------
# Esquemas de Respuesta
# ------------------------


class GameInstanceResponse(BaseModel):
    """Esquema para la respuesta de una instancia de juego"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    game_id: int
    student_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False


class GameInstanceDetailResponse(GameInstanceResponse):
    """Esquema para respuesta detallada de instancia con relaciones"""

    game_title: Optional[str] = None
    student_username: Optional[str] = None


class GameInstanceListResponse(BaseModel):
    """Esquema para listado de instancias de juego"""

    success: bool = True
    message: str = "Instancias obtenidas exitosamente"
    data: List[GameInstanceResponse] = []
    total: int = 0
    skip: int = 0
    limit: int = 10


class SingleGameInstanceResponse(BaseModel):
    """Esquema para respuesta de una sola instancia"""

    success: bool = True
    message: str = "Instancia obtenida exitosamente"
    data: Optional[GameInstanceDetailResponse] = None


class GameInstanceCreateResponse(BaseModel):
    """Esquema para respuesta de creación de instancia"""

    success: bool = True
    message: str = "Instancia creada exitosamente"
    data: GameInstanceResponse


class GameInstanceUpdateResponse(BaseModel):
    """Esquema para respuesta de actualización de instancia"""

    success: bool = True
    message: str = "Instancia actualizada exitosamente"
    data: GameInstanceResponse


class GameInstanceEndResponse(BaseModel):
    """Esquema para respuesta de finalización de instancia"""

    success: bool = True
    message: str = "Instancia finalizada exitosamente"
    data: GameInstanceResponse


class GameInstanceDeleteResponse(BaseModel):
    """Esquema para respuesta de eliminación de instancia"""

    success: bool = True
    message: str = "Instancia eliminada exitosamente"
