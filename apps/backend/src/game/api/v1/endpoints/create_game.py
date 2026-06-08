"""
Endpoint: Create game (admin only)

POST /games/

Administrador puede crear un juego en el catálogo.
Delega en CreateGameUseCase.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps.game_publisher import require_admin_role
from src.game.application.usecase.create_game_usecase import CreateGameUseCase
from src.game.api.v1.schemas.game import (
    GameCreate,
    GameCreateResponse,
    GameResponse,
)


router = APIRouter(prefix="/games")


@router.post(
    "",
    response_model=GameCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea un nuevo juego en el catálogo (admin only)",
)
async def create_game(
    request: GameCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin_role),
):
    """
    Crea un nuevo juego en el catálogo.

    - **title**: Título del juego (requerido)
    - **description**: Descripción del juego (opcional)
    - **creator**: Nombre del creador (opcional)
    - **subject**: Materia/asignatura (opcional)
    - **game_id**: UUID del juego asociado al curso (opcional)

    Validations: no permite duplicados por nombre.
    Requiere rol de administrador.
    """
    usecase = CreateGameUseCase(db)
    return await usecase.execute(request)
