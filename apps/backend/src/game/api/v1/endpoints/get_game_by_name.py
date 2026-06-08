from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import SingleGameResponse, GameDetailResponse


router = APIRouter(prefix="/games", dependencies=[])  # Auth heredado del router padre (HTTPBearer)


@router.get("/by-name/{game_title}", response_model=SingleGameResponse)
async def get_game_by_name(
    game_title: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene un juego por su título.

    - **game_title**: Título del juego a buscar
    """
    game_repo = GameRepository(db)

    game = await game_repo.get_by_name(game_title)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con título '{game_title}' no encontrado",
        )

    # Calcular cantidad de niveles
    levels_count = len(game.levels) if game.levels else 0

    # Crear respuesta detallada
    game_detail = GameDetailResponse.model_validate(game)
    game_detail.levels_count = levels_count

    return SingleGameResponse(data=game_detail)