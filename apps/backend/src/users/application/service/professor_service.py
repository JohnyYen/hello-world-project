# app/services/professor_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.api.v1.schemas.professor import ProfessorCreate, ProfessorUpdate
from src.users.domain.professor import Professor
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class ProfessorService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de profesores.

    Proporciona una capa de abstracción sobre el repositorio de profesores,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = ProfessorRepository(db)
        super().__init__(repository, Professor)
        
