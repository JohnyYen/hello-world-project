# app/services/level_service.py
from src.game.infrastructure.level_repository import LevelRepository
from src.game.domain.level import Level
from src.shared.application.usecase.base_service import BaseService


class LevelService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de niveles.

    Proporciona una capa de abstracción sobre el repositorio de niveles,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: LevelRepository, model: type[Level]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de niveles
            model: Clase del modelo Level
        """
        super().__init__(repository, model)
