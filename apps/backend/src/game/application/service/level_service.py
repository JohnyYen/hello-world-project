# app/services/level_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.level import LevelCreate, LevelUpdate
from src.game.domain.level import Level
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class LevelService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de niveles.

    Proporciona una capa de abstracción sobre el repositorio de niveles,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = LevelRepository(db)
        super().__init__(repository, Level)