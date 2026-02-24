# app/services/metric_type_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.metric_type_repository import MetricTypeRepository
from src.statistic.api.v1.schemas.metric_type import MetricTypeCreate, MetricTypeUpdate
from src.statistic.domain.metric_type import MetricType
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class MetricTypeService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de tipos de métrica.

    Proporciona una capa de abstracción sobre el repositorio de tipos de métrica,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = MetricTypeRepository(db)
        super().__init__(repository, MetricType)