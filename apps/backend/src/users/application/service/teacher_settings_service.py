from typing import Optional

from src.users.infrastructure.teacher_settings_repository import (
    TeacherSettingsRepository,
)
from src.users.domain.teacher_settings import TeacherSettings
from src.shared.application.usecase.base_service import BaseService


class TeacherSettingsService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de configuraciones de profesor.

    Proporciona una capa de abstracción sobre el repositorio de TeacherSettings,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(
        self, repository: TeacherSettingsRepository, model: type[TeacherSettings]
    ):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de configuraciones de profesor
            model: Clase del modelo TeacherSettings
        """
        super().__init__(repository, model)

    async def get_by_user_id(self, user_id: int) -> Optional[TeacherSettings]:
        """
        Obtiene las configuraciones de un profesor por ID de usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[TeacherSettings]: Instancia de TeacherSettings si se encuentra, None en caso contrario
        """
        return await self.repository.get_by_user_id(user_id)

    async def create_for_user(self, user_id: int) -> TeacherSettings:
        """
        Crea nuevas configuraciones para un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            TeacherSettings: Instancia de TeacherSettings creada
        """
        data = {"user_id": user_id}
        return await self.create(data)
