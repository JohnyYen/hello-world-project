# app/services/game_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game import GameCreate, GameUpdate
from src.game.domain.game import Game
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class GameService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de juegos.

    Proporciona una capa de abstracción sobre el repositorio de juegos,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = GameRepository(db)
        super().__init__(repository, Game)