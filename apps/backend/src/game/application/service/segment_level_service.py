# app/services/segment_level_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.api.v1.schemas.segment_level import SegmentLevelCreate, SegmentLevelUpdate
from src.game.domain.segment_level import SegmentLevel
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService

class SegmentLevelService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de segmentos de nivel.

    Proporciona una capa de abstracción sobre el repositorio de segmentos de nivel,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = SegmentLevelRepository(db)
        super().__init__(repository, SegmentLevel)