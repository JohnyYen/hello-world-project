from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.application.service.teacher_settings_service import (
    TeacherSettingsService,
)
from src.users.api.v1.schemas.teacher import (
    TeacherSettingsResponseSchema,
    TeacherSettingsResponse,
)
from src.shared.application.providers.users_providers import (
    get_teacher_settings_service,
)


class GetTeacherSettingsUseCase:
    """
    Caso de uso para obtener las configuraciones del profesor autenticado.

    Responsabilidades:
    - Obtener el usuario actual del JWT token
    - Validar que tenga rol de professor
    - Buscar el registro de TeacherSettings asociado
    - Retornar las configuraciones
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        settings_service: TeacherSettingsService = Depends(
            get_teacher_settings_service
        ),
    ):
        self.db = db
        self.current_user = current_user
        self.settings_service = settings_service

    async def execute(self) -> TeacherSettingsResponseSchema:
        """
        Obtiene las configuraciones del profesor autenticado.

        Returns:
            TeacherSettingsResponseSchema: Configuraciones del profesor

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

        # Validar que el usuario tenga un registro de Professor
        from src.users.infrastructure.professor_repository import ProfessorRepository

        professor_repo = ProfessorRepository(self.db)
        professor = await professor_repo.get_by_user_id(self.current_user.id)

        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe perfil de profesor para este usuario. Contacte al administrador.",
            )

        # Buscar configuraciones de TeacherSettings
        settings = await self.settings_service.get_by_user_id(self.current_user.id)

        if not settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existen configuraciones de profesor para este usuario",
            )

        # Construir respuesta con todos los campos
        # Normalizar "instant" legacy a "realtime"
        freq = settings.notification_frequency
        if freq == "instant":
            freq = "realtime"

        settings_data = TeacherSettingsResponse(
            theme=settings.theme,
            notifications_enabled=settings.notifications_enabled,
            notification_frequency=freq,
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
            message="Configuraciones obtenidas exitosamente",
            data=settings_data,
        )
