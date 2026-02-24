from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.segment_level import (
    SegmentLevelListResponse,
    SegmentLevelResponse,
)


router = APIRouter(prefix="/segments")


@router.get("/{level_id}/segments", response_model=SegmentLevelListResponse)
async def get_level_segments(
    level_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista los segmentos de un nivel con paginación.

    - **level_id**: ID del nivel
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a devolver
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

    # Obtener segmentos
    segments = await segment_repo.get_by_level_id(level_id)

    # Aplicar paginación manual
    total = len(segments)
    paginated_segments = segments[skip : skip + limit]

    # Convertir a respuestas
    segment_responses = [
        SegmentLevelResponse.model_validate(segment) for segment in paginated_segments
    ]

    return SegmentLevelListResponse(
        data=segment_responses,
        total=total,
    )
