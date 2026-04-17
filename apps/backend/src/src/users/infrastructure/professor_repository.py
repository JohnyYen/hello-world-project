from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.professor import Professor


class ProfessorRepository(BaseRepository[Professor]):
    """
    Repositorio específico para el modelo Professor.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Professor)

    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> Optional[Professor]:
        """
        Obtiene un profesor por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye profesores marcados como eliminados

        Returns:
            Professor: Instancia del modelo Professor si se encuentra, None en caso contrario
        """
        filters = {"user_id": user_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_professor_id(
        self, professor_id: str, include_deleted: bool = False
    ) -> Optional[Professor]:
        """
        Obtiene un profesor por ID de profesor.

        Args:
            professor_id: ID del profesor
            include_deleted: Si True, incluye profesores marcados como eliminados

        Returns:
            Professor: Instancia del modelo Professor si se encuentra, None en caso contrario
        """
        filters = {"professor_id": professor_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)
