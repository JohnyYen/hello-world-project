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
from src.shared.application.providers.users_providers import (
    get_teacher_settings_service,
    get_teacher_settings_repository,
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
        settings_service: TeacherSettingsService = Depends(
            get_teacher_settings_service
        ),
        settings_repo: TeacherSettingsRepository = Depends(
            get_teacher_settings_repository
        ),
    ):
        self.db = db
        self.current_user = current_user
        self.settings_service = settings_service
        self.settings_repo = settings_repo

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

        # Actualizar campos (solo los que se proporcionan)
        update_data = {}
        if settings_data.theme is not None:
            update_data["theme"] = settings_data.theme
        if settings_data.notifications_enabled is not None:
            update_data["notifications_enabled"] = settings_data.notifications_enabled
        if settings_data.notification_frequency is not None:
            update_data["notification_frequency"] = settings_data.notification_frequency
        if settings_data.interface_language is not None:
            update_data["interface_language"] = settings_data.interface_language
        # Session settings
        if settings_data.auto_logout is not None:
            update_data["auto_logout"] = settings_data.auto_logout
        if settings_data.session_duration_minutes is not None:
            update_data["session_duration_minutes"] = (
                settings_data.session_duration_minutes
            )
        if settings_data.remember_login is not None:
            update_data["remember_login"] = settings_data.remember_login
        # Appearance settings
        if settings_data.color_theme is not None:
            update_data["color_theme"] = settings_data.color_theme
        if settings_data.animations_enabled is not None:
            update_data["animations_enabled"] = settings_data.animations_enabled
        # Notification settings (extended)
        if settings_data.email_notifications is not None:
            update_data["email_notifications"] = settings_data.email_notifications
        # Language settings (extended)
        if settings_data.date_format is not None:
            update_data["date_format"] = settings_data.date_format
        if settings_data.timezone is not None:
            update_data["timezone"] = settings_data.timezone

        if update_data:
            await self.settings_repo.update(settings.id, update_data)
            # Refrescar para obtener valores actualizados
            settings = await self.settings_repo.get_by_id(settings.id)

        # Construir respuesta con todos los campos
        settings_response = TeacherSettingsResponse(
            theme=settings.theme,
            notifications_enabled=settings.notifications_enabled,
            notification_frequency=settings.notification_frequency,
            interface_language=settings.interface_language,
            # Session settings
            auto_logout=settings.auto_logout,
            session_duration_minutes=settings.session_duration_minutes,
            remember_login=settings.remember_login,
            # Appearance settings
            color_theme=settings.color_theme,
            animations_enabled=settings.animations_enabled,
            # Notification settings (extended)
            email_notifications=settings.email_notifications,
            # Language settings (extended)
            date_format=settings.date_format,
            timezone=settings.timezone,
        )

        return TeacherSettingsResponseSchema(
            success=True,
            message="Configuraciones actualizadas exitosamente",
            data=settings_response,
        )
