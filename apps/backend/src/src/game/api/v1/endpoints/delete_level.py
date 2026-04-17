from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.level import LevelDeleteResponse
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/levels")


@router.delete("/{level_id}", response_model=LevelDeleteResponse)
async def delete_level(
    level_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un nivel (soft delete).

    - **level_id**: ID del nivel a eliminar
    """
    level_repo = LevelRepository(db)

    # Verificar que el nivel existe
    existing_level = await level_repo.get_by_id(level_id)
    if not existing_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nivel con ID {level_id} no encontrado",
        )

    # Soft delete
    await level_repo.delete(level_id)

    return LevelDeleteResponse()
