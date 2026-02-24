from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.api.v1.schemas.segment_level import (
    SegmentLevelUpdate,
    SegmentLevelUpdateResponse,
    SegmentLevelResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


router = APIRouter(prefix="/segments")


@router.put("/{segment_id}", response_model=SegmentLevelUpdateResponse)
async def update_segment(
    segment_id: int,
    segment: SegmentLevelUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza un segmento existente.

    - **segment_id**: ID del segmento a actualizar
    - **configuration**: Nueva configuración JSON (opcional)
    """
    segment_repo = SegmentLevelRepository(db)

    # Verificar que el segmento existe
    existing_segment = await segment_repo.get_by_id(segment_id)
    if not existing_segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Segmento con ID {segment_id} no encontrado",
        )

    try:
        # Filtrar solo campos que no son None
        update_data = {k: v for k, v in segment.model_dump().items() if v is not None}

        if update_data:
            updated_segment = await segment_repo.update(segment_id, update_data)
        else:
            updated_segment = existing_segment

        return SegmentLevelUpdateResponse(
            data=SegmentLevelResponse.model_validate(updated_segment)
        )

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
