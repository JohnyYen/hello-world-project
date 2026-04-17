from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import SingleGameResponse, GameDetailResponse
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/games")


@router.get("/{game_id}", response_model=SingleGameResponse)
async def get_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene los detalles de un juego específico.

    - **game_id**: ID del juego a obtener
    """
    game_repo = GameRepository(db)

    # Obtener juego con niveles (eager loading)
    game = await game_repo.get_by_id_with_levels(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con ID {game_id} no encontrado",
        )

    # Calcular cantidad de niveles
    levels_count = len(game.levels) if game.levels else 0

    # Crear respuesta detallada
    game_detail = GameDetailResponse.model_validate(game)
    game_detail.levels_count = levels_count

    return SingleGameResponse(data=game_detail)
