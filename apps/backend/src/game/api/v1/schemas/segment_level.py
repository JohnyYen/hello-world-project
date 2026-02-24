from datetime import datetime
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ------------------------
# Esquemas de Request
# ------------------------


class SegmentLevelCreate(BaseModel):
    """Esquema para crear un nuevo segmento de nivel"""

    level_id: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None


class SegmentLevelUpdate(BaseModel):
    """Esquema para actualizar un segmento de nivel"""

    configuration: Optional[Dict[str, Any]] = None


# ------------------------
# Esquemas de Respuesta
# ------------------------


class SegmentLevelResponse(BaseModel):
    """Esquema para la respuesta de un segmento de nivel"""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    level_id: int = Field(alias="level_number_id")
    configuration: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False


class SegmentLevelListResponse(BaseModel):
    """Esquema para listado de segmentos de nivel"""

    success: bool = True
    message: str = "Segmentos obtenidos exitosamente"
    data: List[SegmentLevelResponse] = []
    total: int = 0


class SingleSegmentLevelResponse(BaseModel):
    """Esquema para respuesta de un solo segmento de nivel"""

    success: bool = True
    message: str = "Segmento obtenido exitosamente"
    data: Optional[SegmentLevelResponse] = None


class SegmentLevelCreateResponse(BaseModel):
    """Esquema para respuesta de creación de segmento"""

    success: bool = True
    message: str = "Segmento creado exitosamente"
    data: SegmentLevelResponse


class SegmentLevelUpdateResponse(BaseModel):
    """Esquema para respuesta de actualización de segmento"""

    success: bool = True
    message: str = "Segmento actualizado exitosamente"
    data: SegmentLevelResponse


class SegmentLevelDeleteResponse(BaseModel):
    """Esquema para respuesta de eliminación de segmento"""

    success: bool = True
    message: str = "Segmento eliminado exitosamente"
