from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import GameListResponse, GameResponse


router = APIRouter(prefix="/games")


@router.get("", response_model=GameListResponse)
async def get_games(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista todos los juegos con paginación.

    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Número máximo de registros a devolver (1-100)
    """
    game_repo = GameRepository(db)

    # Obtener juegos con sus niveles (eager loading)
    games = await game_repo.get_all_with_levels(skip=skip, limit=limit)

    # Contar total (sin paginación)
    all_games = await game_repo.get_all(include_deleted=False)
    total = len(all_games)

    # Convertir a respuestas con conteo de niveles
    game_responses = []
    for game in games:
        game_data = GameResponse.model_validate(game)
        game_responses.append(game_data)

    return GameListResponse(
        data=game_responses,
        total=total,
        skip=skip,
        limit=limit,
    )
