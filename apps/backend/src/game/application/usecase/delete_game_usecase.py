"""
UseCase: DeleteGameUseCase

Elimina (soft delete) un juego del catálogo.
Solo accesible por administradores.
Valida que el juego no esté asignado a ningún curso.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.game.domain.game import Game
from src.game.infrastructure.game_repository import GameRepository
from src.course.infrastructure.course_repository import CourseRepository
from src.game.api.v1.schemas.game import (
    GameResponse,
    GameDeleteResponse,
)
from src.shared.domain.exceptions import NotFoundException


class DeleteGameUseCase:
    """
    Caso de uso para eliminar un juego del catálogo (soft delete).
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.game_repo = GameRepository(db)
        self.course_repo = CourseRepository(db)

    async def execute(self, game_id: UUID) -> GameDeleteResponse:
        """
        Elimina un juego del catálogo.

        Args:
            game_id: UUID del juego a eliminar.

        Returns:
            GameDeleteResponse con confirmación.

        Raises:
            NotFoundException: Si el juego no existe.
        """
        game = await self.game_repo.get_by_id(game_id, include_deleted=False)
        if not game:
            raise NotFoundException(f"Juego con ID {game_id} no encontrado.")

        # Soft delete
        await self.game_repo.delete(game_id)
        await self.db.commit()

        return GameDeleteResponse(
            message=f"Juego '{game.title}' eliminado exitosamente.",
            game_id=str(game_id),
        )
