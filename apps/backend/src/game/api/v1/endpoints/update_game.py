"""
Endpoint: Update game (admin only)

PUT /games/{game_id}

Administrador puede actualizar un juego del catálogo.
Delega en UpdateGameUseCase.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps.game_publisher import require_admin_role
from src.game.application.usecase.update_game_usecase import UpdateGameUseCase
from src.game.api.v1.schemas.game import GameUpdate, GameUpdateResponse, GameResponse


router = APIRouter(prefix="/games")


@router.put(
    "/{game_id}",
    response_model=GameUpdateResponse,
    summary="Actualiza un juego del catálogo (admin only)",
)
async def update_game(
    game_id: UUID,
    game: GameUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin_role),
):
    """
    Actualiza un juego existente. Todos los campos son opcionales (PATCH-like).

    - **game_id**: UUID del juego a actualizar
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **creator**: Nuevo creador (opcional)
    - **subject**: Nueva materia (opcional)

    Requiere rol de administrador.
    """
    usecase = UpdateGameUseCase(db)
    return await usecase.execute(game_id, game)
