# app/services/game_instance_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.api.v1.schemas.game_instance import GameInstanceCreate, GameInstanceUpdate
from src.game.domain.game_instance import GameInstance
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class GameInstanceService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de instancias de juego.

    Proporciona una capa de abstracción sobre el repositorio de instancias de juego,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = GameInstanceRepository(db)
        super().__init__(repository, GameInstance)