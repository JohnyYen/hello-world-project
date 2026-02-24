from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import GameDeleteResponse
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/games")


@router.delete("/{game_id}", response_model=GameDeleteResponse)
async def delete_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un juego (soft delete).

    - **game_id**: ID del juego a eliminar
    """
    game_repo = GameRepository(db)

    # Verificar que el juego existe
    existing_game = await game_repo.get_by_id(game_id)
    if not existing_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con ID {game_id} no encontrado",
        )

    # Soft delete
    await game_repo.delete(game_id)

    return GameDeleteResponse()
