from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.application.service.teacher_settings_service import (
    TeacherSettingsService,
)
from src.users.infrastructure.teacher_settings_repository import (
    TeacherSettingsRepository,
)
from src.users.api.v1.schemas.teacher import (
    TeacherSettingsUpdate,
    TeacherSettingsResponseSchema,
    TeacherSettingsResponse,
)


class UpdateTeacherSettingsUseCase:
    """
    Caso de uso para actualizar las configuraciones del profesor autenticado.

    Responsabilidades:
    - Obtener el usuario actual del JWT token
    - Validar que tenga rol de professor
    - Buscar el registro de TeacherSettings asociado
    - Actualizar las configuraciones
    - Retornar las configuraciones actualizadas
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user
        self.settings_service = TeacherSettingsService(db)
        self.settings_repo = TeacherSettingsRepository(db)

    async def execute(
        self, settings_data: TeacherSettingsUpdate
    ) -> TeacherSettingsResponseSchema:
        """
        Actualiza las configuraciones del profesor autenticado.

        Args:
            settings_data: Datos a actualizar

        Returns:
            TeacherSettingsResponseSchema: Configuraciones actualizadas

        Raises:
            HTTPException 403: Si el usuario no tiene rol de professor
            HTTPException 404: Si no existen configuraciones de profesor
        """
        # Validar que el usuario tenga rol de professor
        if (
            not self.current_user.role
            or self.current_user.role.role_name != "professor"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no tiene permisos de profesor",
            )

        # Buscar configuraciones de TeacherSettings
        settings = await self.settings_service.get_by_user_id(self.current_user.id)

        if not settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existen configuraciones de profesor para este usuario",
            )

        # Actualizar campos
        update_data = {}
        if settings_data.theme is not None:
            update_data["theme"] = settings_data.theme
        if settings_data.notifications_enabled is not None:
            update_data["notifications_enabled"] = settings_data.notifications_enabled
        if settings_data.notification_frequency is not None:
            update_data["notification_frequency"] = settings_data.notification_frequency
        if settings_data.interface_language is not None:
            update_data["interface_language"] = settings_data.interface_language

        if update_data:
            await self.settings_repo.update(settings.id, update_data)
            # Refrescar para obtener valores actualizados
            settings = await self.settings_repo.get_by_id(settings.id)

        # Construir respuesta
        settings_response = TeacherSettingsResponse(
            theme=settings.theme,
            notifications_enabled=settings.notifications_enabled,
            notification_frequency=settings.notification_frequency,
            interface_language=settings.interface_language,
        )

        return TeacherSettingsResponseSchema(
            success=True,
            message="Configuraciones actualizadas exitosamente",
            data=settings_response,
        )
