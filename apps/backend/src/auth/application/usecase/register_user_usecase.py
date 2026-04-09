from datetime import timedelta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.config import settings
from src.shared.infrastructure.session import get_db
from src.shared.application.providers.users_providers import (
    get_user_service,
    get_teacher_settings_service,
)
from src.auth.infrastructure.security import create_access_token
from src.users.application.service.user_service import UserService
from src.users.application.service.teacher_settings_service import (
    TeacherSettingsService,
)
from src.users.infrastructure.role_repository import RoleRepository
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.domain.professor import Professor
from src.shared.domain.exceptions import DuplicateEntryException
from src.users.api.v1.schemas.user import UserCreate, UserResponse, UserLoginResponse


class RegisterUserUseCase:
    """
    Caso de uso para registrar un nuevo usuario.

    Responsabilidades:
    - Validar unicidad de email y username (delegado a UserService)
    - Asignar automáticamente el rol de 'professor' al nuevo usuario
    - Crear usuario con contraseña hasheada (delegado a UserService)
    - Generar token JWT de acceso para el usuario recién creado
    - Crear TeacherSettings automáticamente si el rol es professor
    - Devolver respuesta de login con token y usuario

    Este UseCase NO maneja:
    - Activación de cuenta (por email, SMS, etc.)
    - Envío de email de bienvenida
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        teacher_settings_service: TeacherSettingsService = Depends(
            get_teacher_settings_service
        ),
    ):
        self.db = db
        self.user_service = user_service
        self.teacher_settings_service = teacher_settings_service
        self.role_repository = RoleRepository(db)
        self.professor_repository = ProfessorRepository(db)

    async def execute(self, user_data: UserCreate) -> UserLoginResponse:
        """
        Ejecuta el flujo de registro de usuario.

        Args:
            user_data: Datos validados para la creación del usuario

        Returns:
            UserLoginResponse: Respuesta con token JWT y datos del usuario creado

        Raises:
            DuplicateEntryException: Si el email o username ya existen
            NotFoundException: Si el rol 'professor' no existe en la base de datos
        """
        # 1. Obtener el rol de professor
        professor_role = await self.role_repository.get_professor_role()
        professor_role_id = professor_role.id  # type: ignore[attr-defined]

        # 2. Crear usuario con el rol de professor asignado automáticamente
        user = await self.user_service.create_user(
            user_data=user_data,
            role_id=professor_role_id,
        )

        # 3. Crear Professor profile automáticamente para profesores
        professor = Professor(user_id=user.id, department="General")
        self.db.add(professor)
        await self.db.flush()  # Get the professor ID without committing

        # 4. Crear TeacherSettings automáticamente para profesores
        await self.teacher_settings_service.create_for_user(user.id)

        # 5. Obtener el usuario creado con la relación role cargada de forma eager
        user_with_role = await self.user_service.get_user_by_id_with_role(user.id)

        # 6. Generar token JWT para el nuevo usuario
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # 7. Devolver respuesta con token y usuario
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            user=UserResponse.model_validate(user_with_role),
        )
