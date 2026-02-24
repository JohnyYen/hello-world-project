# app/services/progress_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.api.v1.schemas.progress import ProgressCreate, ProgressUpdate
from src.statistic.domain.progress import Progress
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class ProgressService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de progresos.

    Proporciona una capa de abstracción sobre el repositorio de progresos,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = ProgressRepository(db)
        super().__init__(repository, Progress)
