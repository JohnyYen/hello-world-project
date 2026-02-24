from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.users.api.v1.schemas.student import StudentListResponse, StudentResponse


class ListStudentsUseCase:
    """
    Caso de uso para listar estudiantes.

    Responsabilidades:
    - Validar que el usuario actual sea professor o admin
    - Obtener lista de usuarios con rol de student
    - Retornar datos combinados de User + Student
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(
        self, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> StudentListResponse:
        """
        Lista todos los estudiantes.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros
            search: Búsqueda por nombre, email o username

        Returns:
            StudentListResponse: Lista de estudiantes

        Raises:
            HTTPException 403: Si no tiene permisos de professor o admin
        """
        # Validar rol
        if self.current_user.role.role_name not in ["admin", "professor"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver estudiantes",
            )

        # Buscar usuarios con rol de student
        user_repo = UserRepository(self.db)
        students = await user_repo.get_students_with_pagination(
            skip=skip, limit=limit, search=search
        )

        # Construir respuesta
        student_responses = []
        for student in students:
            student_response = StudentResponse(
                id=student.id,
                username=student.username,
                email=student.email,
                name=student.name,
                lastname=student.lastname,
                is_active=student.is_active,
                created_at=student.created_at,
                updated_at=student.updated_at,
            )
            student_responses.append(student_response)

        return StudentListResponse(
            success=True,
            message="Estudiantes listados exitosamente",
            data=student_responses,
        )
