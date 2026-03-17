# app/services/segment_level_service.py
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.domain.segment_level import SegmentLevel
from src.shared.application.usecase.base_service import BaseService


class SegmentLevelService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de segmentos de nivel.

    Proporciona una capa de abstracción sobre el repositorio de segmentos de nivel,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: SegmentLevelRepository, model: type[SegmentLevel]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de segmentos de nivel
            model: Clase del modelo SegmentLevel
        """
        super().__init__(repository, model)
