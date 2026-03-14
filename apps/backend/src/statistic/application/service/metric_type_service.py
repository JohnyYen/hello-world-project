# app/services/metric_type_service.py
from src.statistic.infrastructure.metric_type_repository import MetricTypeRepository
from src.statistic.domain.metric_type import MetricType
from src.shared.application.usecase.base_service import BaseService


class MetricTypeService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de tipos de métrica.

    Proporciona una capa de abstracción sobre el repositorio de tipos de métrica,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: MetricTypeRepository, model: type[MetricType]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de tipos de métrica
            model: Clase del modelo MetricType
        """
        super().__init__(repository, model)
