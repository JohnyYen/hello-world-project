"""
UseCase: UpdateGameUseCase

Orquesta la actualización parcial de un juego del catálogo.
Delega en GameService.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.game.domain.game import Game
from src.game.infrastructure.game_repository import GameRepository
from src.game.application.usecase.create_game_usecase import GameService
from src.game.api.v1.schemas.game import (
    GameUpdate,
    GameResponse,
    GameUpdateResponse,
)
from src.shared.domain.exceptions import NotFoundException


class UpdateGameUseCase:
    """
    Caso de uso para actualizar un juego existente.

    Soporta actualización parcial (campos opcionales).
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = GameRepository(db)
        self.service = GameService(self.repo, Game)

    async def execute(self, game_id: UUID, request: GameUpdate) -> GameUpdateResponse:
        """
        Actualiza los campos enviados de un juego. Campos no enviados se mantienen.

        Args:
            game_id: UUID del juego a actualizar.
            request: Schema con los campos a modificar (todos opcionales).

        Returns:
            GameUpdateResponse con el juego actualizado.

        Raises:
            NotFoundException: Si el juego no existe.
        """
        game = await self.repo.get_by_id(game_id, include_deleted=False)
        if not game:
            raise NotFoundException(f"Juego con ID {game_id} no encontrado.")

        update_data = request.model_dump(exclude_none=True, by_alias=True)
        if not update_data:
            raise ValueError("No se proporcionaron datos para actualizar.")

        updated = await self.service.update(game_id, update_data)
        return GameUpdateResponse(data=GameResponse.model_validate(updated))
