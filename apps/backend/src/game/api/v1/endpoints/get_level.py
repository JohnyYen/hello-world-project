from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.level import SingleLevelResponse, LevelDetailResponse


router = APIRouter(prefix="/levels")


@router.get("/{level_id}", response_model=SingleLevelResponse)
async def get_level(
    level_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene los detalles de un nivel específico.

    - **level_id**: ID del nivel a obtener
    """
    level_repo = LevelRepository(db)

    # Obtener nivel con segmentos (eager loading)
    level = await level_repo.get_by_id_with_segments(level_id)

    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nivel con ID {level_id} no encontrado",
        )

    # Calcular cantidad de segmentos
    segments_count = len(level.segments) if level.segments else 0

    # Crear respuesta detallada
    level_detail = LevelDetailResponse.model_validate(level)
    level_detail.segments_count = segments_count

    return SingleLevelResponse(data=level_detail)
