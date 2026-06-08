"""
UseCase: CreateGameUseCase

Orquesta la creación de un juego en el catálogo.
Solo accesible por administradores.
Valida duplicados por nombre, delega al GameService.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.game.domain.game import Game
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import (
    GameCreate,
    GameCreateResponse,
    GameResponse,
)
from src.shared.domain.exceptions import DuplicateEntryException
from src.shared.application.usecase.base_service import BaseService


class GameService(BaseService[Game]):
    """
    Servicio CRUD para el modelo Game.

    Hereda operaciones genéricas de BaseService y agrega métodos específicos.
    """

    # No se agrega lógica adicional por ahora — el modelo lo extiende si es necesario.
    pass


class CreateGameUseCase:
    """
    Caso de uso para crear un nuevo juego en el catálogo.

    Flujo:
    1. Verifica que no exista otro juego con el mismo nombre.
    2. Crea el juego delegando en GameService.
    3. Retorna la representación del juego creado.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = GameRepository(db)
        self.service = GameService(self.repo, Game)

    async def execute(self, request: GameCreate) -> GameCreateResponse:
        """
        Crear un nuevo juego en el catálogo.

        Args:
            request: Schema con los datos del juego a crear.

        Returns:
            GameCreateResponse con el juego creado.

        Raises:
            DuplicateEntryException: Si ya existe un juego con el mismo nombre.
        """
        existing = await self.repo.get_by_name(request.title)
        if existing:
            raise DuplicateEntryException(
                f"Ya existe un juego con el nombre '{request.title}'."
            )

        game_data = request.model_dump(exclude_none=True)
        new_game = await self.service.create(game_data)
        await self.db.refresh(new_game)

        return GameCreateResponse(data=GameResponse.model_validate(new_game))
