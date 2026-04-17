from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import GameUpdate, GameUpdateResponse, GameResponse
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


router = APIRouter(prefix="/games")


@router.put("/{game_id}", response_model=GameUpdateResponse)
async def update_game(
    game_id: int,
    game: GameUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza un juego existente.

    - **game_id**: ID del juego a actualizar
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **creator**: Nuevo creador (opcional)
    - **subject**: Nueva materia (opcional)
    - **publication_status**: Nuevo estado (opcional)
    """
    game_repo = GameRepository(db)

    # Verificar que el juego existe
    existing_game = await game_repo.get_by_id(game_id)
    if not existing_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con ID {game_id} no encontrado",
        )

    try:
        # Filtrar solo campos que no son None
        update_data = {k: v for k, v in game.model_dump().items() if v is not None}

        if update_data:
            updated_game = await game_repo.update(game_id, update_data)
        else:
            updated_game = existing_game

        return GameUpdateResponse(data=GameResponse.model_validate(updated_game))

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
