from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.teacher_settings import TeacherSettings


class TeacherSettingsRepository(BaseRepository[TeacherSettings]):
    """
    Repositorio específico para el modelo TeacherSettings.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, TeacherSettings)

    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> Optional[TeacherSettings]:
        """
        Obtiene las configuraciones de un profesor por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye settings marcados como eliminados

        Returns:
            TeacherSettings: Instancia del modelo si se encuentra, None en caso contrario
        """
        filters = {"user_id": user_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)
