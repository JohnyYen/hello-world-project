from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.level import (
    LevelCreate,
    LevelCreateResponse,
    LevelResponse,
)
from src.shared.domain.exceptions import DuplicateEntryException


router = APIRouter(prefix="/games/{game_id}/levels")


@router.post(
    "", response_model=LevelCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_game_level(
    game_id: int,
    level: LevelCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Crea un nuevo nivel en un juego.

    - **game_id**: ID del juego
    - **level_number**: Número del nivel (requerido)
    - **title**: Título del nivel (requerido)
    - **description**: Descripción del nivel (opcional)
    - **goal**: Objetivo del nivel (opcional)
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

    try:
        # Crear nivel
        level_data = level.model_dump()
        level_data["game_id"] = game_id  # Set game_id from URL path
        new_level = await level_repo.create(level_data)

        return LevelCreateResponse(data=LevelResponse.model_validate(new_level))

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
