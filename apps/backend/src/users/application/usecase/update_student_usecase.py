from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.users.api.v1.schemas.student import StudentUpdate, StudentResponse


class UpdateStudentUseCase:
    """
    Caso de uso para actualizar un estudiante.

    Responsabilidades:
    - Validar que el usuario actual sea professor o admin
    - Verificar que el estudiante exista
    - Actualizar datos del usuario
    - Retornar datos actualizados
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(
        self, student_id: int, student_data: StudentUpdate
    ) -> StudentResponse:
        """
        Actualiza un estudiante.

        Args:
            student_id: ID del estudiante a actualizar
            student_data: Datos a actualizar

        Returns:
            StudentResponse: Datos del estudiante actualizado

        Raises:
            HTTPException 403: Si no tiene permisos
            HTTPException 404: Si el estudiante no existe
        """
        # Validar rol
        if self.current_user.role.role_name not in ["admin", "professor"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para actualizar estudiantes",
            )

        # Buscar usuario
        user_repo = UserRepository(self.db)
        student = await user_repo.get_by_id(student_id)

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

        # Preparar datos para actualizar
        update_data = {}
        if student_data.username is not None:
            update_data["username"] = student_data.username
        if student_data.email is not None:
            update_data["email"] = student_data.email
        if student_data.name is not None:
            update_data["name"] = student_data.name
        if student_data.lastname is not None:
            update_data["lastname"] = student_data.lastname
        if student_data.is_active is not None:
            update_data["is_active"] = student_data.is_active

        # Actualizar usuario
        if update_data:
            await user_repo.update(student_id, update_data)
            # Refrescar para obtener datos actualizados
            student = await user_repo.get_by_id(student_id)

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
        )
