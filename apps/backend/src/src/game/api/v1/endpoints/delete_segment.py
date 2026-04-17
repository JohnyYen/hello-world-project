from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.api.v1.schemas.segment_level import SegmentLevelDeleteResponse
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/segments")


@router.delete("/{segment_id}", response_model=SegmentLevelDeleteResponse)
async def delete_segment(
    segment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un segmento (soft delete).

    - **segment_id**: ID del segmento a eliminar
    """
    segment_repo = SegmentLevelRepository(db)

    # Verificar que el segmento existe
    existing_segment = await segment_repo.get_by_id(segment_id)
    if not existing_segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Segmento con ID {segment_id} no encontrado",
        )

    # Soft delete
    await segment_repo.delete(segment_id)

    return SegmentLevelDeleteResponse()
