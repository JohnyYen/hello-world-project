from typing import List, Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
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
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        course_id: Optional[UUID] = None,
        school_year: Optional[str] = None,
    ) -> StudentListResponse:
        """
        Lista todos los estudiantes.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros
            search: Búsqueda por nombre, email o username
            course_id: Filtrar estudiantes por ID de curso (opcional)
            school_year: Filtrar por curso escolar (ej: '2025 a 2026') (opcional)

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
            skip=skip, limit=limit, search=search, course_id=course_id, school_year=school_year
        )

        # Obtener repositorio de game_instances para calcular last_activity
        game_instance_repo = GameInstanceRepository(self.db)

        # Construir respuesta
        student_responses = []
        for student in students:
            # Calcular last_activity desde game_instances
            last_activity = None
            try:
                instances = await game_instance_repo.get_by_student_id(student.id)
                if instances:
                    # Obtener la fecha más reciente de activity (created_at o updated_at)
                    last_activity = max(
                        (i.updated_at or i.created_at for i in instances if i.updated_at or i.created_at),
                        default=None
                    )
            except Exception:
                # Si falla, продолжаем sin last_activity
                pass

            student_response = StudentResponse(
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
            student_responses.append(student_response)

        return StudentListResponse(
            success=True,
            message="Estudiantes listados exitosamente",
            data=student_responses,
        )
