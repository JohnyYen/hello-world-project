from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.student import Student


class StudentRepository(BaseRepository[Student]):
    """
    Repositorio específico para el modelo Student.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Student)

    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> Optional[Student]:
        """
        Obtiene un estudiante por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye estudiantes marcados como eliminados

        Returns:
            Student: Instancia del modelo Student si se encuentra, None en caso contrario
        """
        filters = {"user_id": user_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_student_id(
        self, student_id: str, include_deleted: bool = False
    ) -> Optional[Student]:
        """
        Obtiene un estudiante por ID de estudiante.

        Args:
            student_id: ID del estudiante
            include_deleted: Si True, incluye estudiantes marcados como eliminados

        Returns:
            Student: Instancia del modelo Student si se encuentra, None en caso contrario
        """
        filters = {"student_id": student_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)
