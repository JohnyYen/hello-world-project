from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.users.api.v1.schemas.student import StudentResponse


class DeleteStudentUseCase:
    """
    Caso de uso para eliminar (soft delete) un estudiante.

    Responsabilidades:
    - Validar que el usuario actual sea professor o admin
    - Verificar que el estudiante exista
    - Realizar soft delete del usuario
    - Retornar mensaje de éxito
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self, student_id: int) -> dict:
        """
        Elimina (soft delete) un estudiante.

        Args:
            student_id: ID del estudiante a eliminar

        Returns:
            dict: Mensaje de éxito

        Raises:
            HTTPException 403: Si no tiene permisos
            HTTPException 404: Si el estudiante no existe
        """
        # Validar rol
        if self.current_user.role.role_name not in ["admin", "professor"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para eliminar estudiantes",
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

        # Realizar soft delete
        await user_repo.soft_delete(student_id)

        return {
            "success": True,
            "message": f"Estudiante con ID {student_id} eliminado exitosamente",
        }
