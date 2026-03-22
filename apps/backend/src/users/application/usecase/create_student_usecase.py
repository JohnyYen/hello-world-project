from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.users.infrastructure.role_repository import RoleRepository
from src.users.infrastructure.teacher_settings_repository import (
    TeacherSettingsRepository,
)
from src.users.application.service.teacher_settings_service import (
    TeacherSettingsService,
)
from src.users.domain.teacher_settings import TeacherSettings
from src.users.api.v1.schemas.student import StudentCreate, StudentResponse


class CreateStudentUseCase:
    """
    Caso de uso para crear un nuevo estudiante.

    Responsabilidades:
    - Validar que el usuario actual sea professor o admin
    - Crear User con rol de student
    - Crear Student asociado
    - Crear StudentSettings automáticamente
    - Retornar datos del estudiante creado
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self, student_data: StudentCreate) -> StudentResponse:
        """
        Crea un nuevo estudiante.

        Args:
            student_data: Datos del estudiante a crear

        Returns:
            StudentResponse: Datos del estudiante creado

        Raises:
            HTTPException 403: Si no tiene permisos
            HTTPException 409: Si email o username ya existen
        """
        # Validar rol
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Current user role: {self.current_user.role}")
        logger.info(
            f"Role name: {self.current_user.role.role_name if self.current_user.role else 'None'}"
        )
        if self.current_user.role.role_name not in ["admin", "professor"]:
            logger.warning(
                f"User {self.current_user.username} with role {self.current_user.role.role_name} attempted to create student"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para crear estudiantes",
            )

        # Obtener rol de student
        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()
        student_role_id = int(student_role.id)

        # Preparar datos para crear usuario
        user_data = {
            "username": student_data.username,
            "email": student_data.email,
            "name": student_data.name,
            "lastname": student_data.lastname,
            "password": student_data.password,
            "role_id": student_role_id,
            "is_active": student_data.is_active
            if student_data.is_active is not None
            else True,
        }

        # Crear usuario
        user_repo = UserRepository(self.db)
        user = await user_repo.create(user_data)

        # Crear registro de Student
        student_repo = StudentRepository(self.db)
        await student_repo.create({"user_id": user.id})

        # Crear StudentSettings automáticamente
        settings_service = TeacherSettingsService(
            TeacherSettingsRepository(self.db), TeacherSettings
        )
        await settings_service.create_for_user(user.id)

        # Refrescar usuario para obtener relaciones
        await user_repo.db.refresh(user)

        # Construir respuesta
        return StudentResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            name=user.name,
            lastname=user.lastname,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
