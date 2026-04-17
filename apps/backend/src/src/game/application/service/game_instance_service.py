# app/services/game_instance_service.py
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.domain.game_instance import GameInstance
from src.shared.application.usecase.base_service import BaseService


class GameInstanceService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de instancias de juego.

    Proporciona una capa de abstracción sobre el repositorio de instancias de juego,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: GameInstanceRepository, model: type[GameInstance]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de instancias de juego
            model: Clase del modelo GameInstance
        """
        super().__init__(repository, model)
