# app/services/progress_service.py
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress
from src.shared.application.usecase.base_service import BaseService


class ProgressService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de progresos.

    Proporciona una capa de abstracción sobre el repositorio de progresos,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: ProgressRepository, model: type[Progress]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de progresos
            model: Clase del modelo Progress
        """
        super().__init__(repository, model)
