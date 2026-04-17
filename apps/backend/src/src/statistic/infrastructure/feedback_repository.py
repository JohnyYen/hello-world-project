from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.statistic.domain.feedback import Feedback


class FeedbackRepository(BaseRepository[Feedback]):
    """
    Repositorio específico para el modelo Feedback.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Feedback)

    async def get_by_student_id(
        self, student_id: int, include_deleted: bool = False
    ) -> List[Feedback]:
        """
        Obtiene feedback por ID de estudiante.

        Args:
            student_id: ID del estudiante
            include_deleted: Si True, incluye feedback marcados como eliminados

        Returns:
            List[Feedback]: Lista de feedback
        """
        filters = {"student_id": student_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_rating(
        self, rating: int, include_deleted: bool = False
    ) -> List[Feedback]:
        """
        Obtiene feedback por calificación.

        Args:
            rating: Calificación del feedback
            include_deleted: Si True, incluye feedback marcados como eliminados

        Returns:
            List[Feedback]: Lista de feedback
        """
        filters = {"rating": rating}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_all_with_student(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: str = "created_at",
        descending: bool = True,
    ) -> List[Feedback]:
        """
        Obtiene todo el feedback con información del estudiante.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye feedback eliminados
            order_by: Campo por el cual ordenar
            descending: Si True, ordena en forma descendente

        Returns:
            List[Feedback]: Lista de feedback
        """
        return await self.get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            order_by=order_by,
            descending=descending,
        )
