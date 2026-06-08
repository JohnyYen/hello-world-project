"""
Endpoint: Delete game (admin only)

DELETE /games/{game_id}

Administrador puede eliminar un juego del catálogo (soft delete).
Delega en DeleteGameUseCase.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps.game_publisher import require_admin_role
from src.game.application.usecase.delete_game_usecase import DeleteGameUseCase
from src.game.api.v1.schemas.game import GameDeleteResponse


router = APIRouter(prefix="/games")


@router.delete(
    "/{game_id}",
    response_model=GameDeleteResponse,
    summary="Elimina un juego (soft delete, admin only)",
)
async def delete_game(
    game_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin_role),
):
    """
    Elimina un juego del catálogo (soft delete).

    - **game_id**: UUID del juego a eliminar

    Requiere rol de administrador.
    """
    usecase = DeleteGameUseCase(db)
    return await usecase.execute(game_id)
