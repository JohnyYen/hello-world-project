from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.users.api.v1.schemas.student import StudentResponse


class GetStudentDetailUseCase:
    """
    Caso de uso para obtener el detalle de un estudiante.

    Responsabilidades:
    - Validar que el usuario actual sea professor, admin, o el propio estudiante
    - Buscar el estudiante por ID
    - Retornar datos del estudiante
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self, student_id: UUID) -> StudentResponse:
        """
        Obtiene el detalle de un estudiante.

        Args:
            student_id: UUID del estudiante a buscar

        Returns:
            StudentResponse: Datos del estudiante

        Raises:
            HTTPException 403: Si no tiene permisos
            HTTPException 404: Si el estudiante no existe
        """
        # Verificar permisos: admin, professor, o el propio estudiante
        is_admin_or_professor = self.current_user.role.role_name in [
            "admin",
            "professor",
        ]
        is_own_profile = self.current_user.id == student_id

        if not is_admin_or_professor and not is_own_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver este estudiante",
            )

        # Buscar usuario
        user_repo = UserRepository(self.db)
        student = await user_repo.get_by_id_with_role(student_id)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        # Verificar que sea estudiante
        if not student.role or student.role.role_name != "student":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario no es un estudiante",
            )

        # Calcular last_activity desde game_instances
        last_activity = None
        try:
            game_instance_repo = GameInstanceRepository(self.db)
            instances = await game_instance_repo.get_by_student_id(student.id)
            if instances:
                last_activity = max(
                    (i.updated_at or i.created_at for i in instances if i.updated_at or i.created_at),
                    default=None
                )
        except Exception:
            # Si falla, continuamos sin last_activity
            pass

        # Construir respuesta
        return StudentResponse(
            id=student.id,
            username=student.username,
            email=student.email,
            name=student.name,
            lastname=student.lastname,
            is_active=student.is_active,
            created_at=student.created_at,
            updated_at=student.updated_at,
            last_activity=last_activity,
        )
