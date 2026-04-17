from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import GameCreate, GameCreateResponse, GameResponse
from src.shared.domain.exceptions import DuplicateEntryException


router = APIRouter(prefix="/games")


@router.post("", response_model=GameCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    game: GameCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Crea un nuevo juego.

    - **title**: Título del juego (requerido)
    - **description**: Descripción del juego (opcional)
    - **creator**: Creador del juego (opcional)
    - **subject**: Materia/asignatura (opcional)
    - **publication_status**: Estado de publicación (opcional)
    """
    game_repo = GameRepository(db)

    try:
        # Crear juego
        game_data = game.model_dump()
        new_game = await game_repo.create(game_data)

        return GameCreateResponse(data=GameResponse.model_validate(new_game))

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
