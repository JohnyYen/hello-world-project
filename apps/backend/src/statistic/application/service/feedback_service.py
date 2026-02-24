# app/services/feedback_service.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.feedback_repository import FeedbackRepository
from src.statistic.domain.feedback import Feedback
from src.shared.application.usecase.base_service import BaseService


class FeedbackService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de feedback.

    Proporciona una capa de abstracción sobre el repositorio de feedback,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        repository = FeedbackRepository(db)
        super().__init__(repository, Feedback)

    async def get_by_student_id(
        self,
        student_id: int,
        include_deleted: bool = False,
    ):
        """
        Obtiene feedback por ID de estudiante.

        Args:
            student_id: ID del estudiante
            include_deleted: Si True, incluye feedback eliminados

        Returns:
            Lista de Feedback
        """
        return await self.repository.get_by_student_id(
            student_id=student_id, include_deleted=include_deleted
        )
