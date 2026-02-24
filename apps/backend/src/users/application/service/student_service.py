# app/services/student_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.users.infrastructure.student_repository import StudentRepository
from src.users.api.v1.schemas.student import StudentCreate, StudentUpdate
from src.users.domain.student import Student
from src.shared.domain.exceptions import NotFoundException
from src.shared.application.usecase.base_service import BaseService


class StudentService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de estudiantes.

    Proporciona una capa de abstracción sobre el repositorio de estudiantes,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = StudentRepository(db)
        super().__init__(repository, Student)
