from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.level import LevelListResponse, LevelResponse


router = APIRouter(prefix="/games/{game_id}/levels")


@router.get("", response_model=LevelListResponse)
async def get_game_levels(
    game_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista los niveles de un juego con paginación.

    - **game_id**: ID del juego
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a devolver
    """
    # Verificar que el juego existe
    game_repo = GameRepository(db)
    game = await game_repo.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con ID {game_id} no encontrado",
        )

    level_repo = LevelRepository(db)

    # Obtener niveles con segmentos (eager loading)
    levels = await level_repo.get_by_game_id_with_segments(game_id)

    # Aplicar paginación manual
    total = len(levels)
    paginated_levels = levels[skip : skip + limit]

    # Convertir a respuestas
    level_responses = [
        LevelResponse.model_validate(level) for level in paginated_levels
    ]

    return LevelListResponse(
        data=level_responses,
        total=total,
    )
