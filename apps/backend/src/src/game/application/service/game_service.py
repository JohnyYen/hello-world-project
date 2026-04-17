# app/services/game_service.py
from src.game.infrastructure.game_repository import GameRepository
from src.game.domain.game import Game
from src.shared.application.usecase.base_service import BaseService


class GameService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de juegos.

    Proporciona una capa de abstracción sobre el repositorio de juegos,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: GameRepository, model: type[Game]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de juegos
            model: Clase del modelo Game
        """
        super().__init__(repository, model)
