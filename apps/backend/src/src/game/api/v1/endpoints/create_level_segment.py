from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.segment_level import (
    SegmentLevelCreate,
    SegmentLevelCreateResponse,
    SegmentLevelResponse,
)
from src.shared.domain.exceptions import DuplicateEntryException


router = APIRouter(prefix="/segments")


@router.post(
    "/{level_id}/segments",
    response_model=SegmentLevelCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_level_segment(
    level_id: int,
    segment: SegmentLevelCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Crea un nuevo segmento en un nivel.

    - **level_id**: ID del nivel
    - **configuration**: Configuración JSON del segmento (opcional)
    """
    # Verificar que el nivel existe
    level_repo = LevelRepository(db)
    level = await level_repo.get_by_id(level_id)
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nivel con ID {level_id} no encontrado",
        )

    segment_repo = SegmentLevelRepository(db)

    try:
        # Crear segmento
        segment_data = segment.model_dump(exclude={"level_id"})
        segment_data["level_number_id"] = level_id  # Usar level_number_id del modelo
        new_segment = await segment_repo.create(segment_data)

        return SegmentLevelCreateResponse(
            data=SegmentLevelResponse.model_validate(new_segment)
        )

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
