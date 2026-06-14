from typing import List, Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.domain.student_activity_log import StudentActivityLog
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.infrastructure.xapi_statement_repository import XAPIStatementRepository
from src.users.api.v1.schemas.student import StudentListResponse, StudentResponse


class ListStudentsUseCase:
    """
    Caso de uso para listar estudiantes.

    Responsabilidades:
    - Validar que el usuario actual sea professor o admin
    - Si es profesor, filtrar solo estudiantes inscritos en sus cursos
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

        # Si es profesor, filtrar solo estudiantes en sus cursos
        professor_user_id = None
        if self.current_user.role.role_name == "professor":
            professor_user_id = self.current_user.id

        # Buscar usuarios con rol de student
        user_repo = UserRepository(self.db)
        students = await user_repo.get_students_with_pagination(
            skip=skip, limit=limit, search=search, course_id=course_id,
            school_year=school_year, professor_user_id=professor_user_id
        )

        # Obtener repositorios para calcular last_activity
        progress_repo = ProgressRepository(self.db)
        xapi_repo = XAPIStatementRepository(self.db)
        student_repo_inst = StudentRepository(self.db)

        # Construir respuesta
        student_responses = []
        for student in students:
            # Resolver students.id (tablas como game_instances, progresses,
            # xapi_statements referencian students.id, NO users.id)
            student_record = await student_repo_inst.get_by_user_id(student.id)
            student_db_id = student_record.id if student_record else None

            # Calcular last_activity desde fuentes de actividad REAL del estudiante.
            # Excluimos game_instances porque se crean automáticamente al asignar un juego
            # y NO representan interacción real del estudiante.
            last_activity = None

            # 1. progresses.updated_at (FK a students.id) — xAPI pipeline
            if student_db_id:
                try:
                    progress_records = await progress_repo.get_by_student_id(student_db_id)
                    if progress_records:
                        progress_activity = max(
                            (p.updated_at for p in progress_records if p.updated_at),
                            default=None
                        )
                        if progress_activity and (not last_activity or progress_activity > last_activity):
                            last_activity = progress_activity
                except Exception:
                    pass

            # 3. xapi_statements.timestamp (FK a students.id) — dato MÁS fresco
            if student_db_id:
                try:
                    xapi_records = await xapi_repo.get_by_student_id(
                        student_db_id, skip=0, limit=1
                    )
                    if xapi_records:
                        xapi_ts = xapi_records[0].timestamp
                        if xapi_ts and (not last_activity or xapi_ts > last_activity):
                            last_activity = xapi_ts
                except Exception:
                    pass

            # 4. student_activity_log.occurred_at (FK a users.id)
            try:
                log_query = (
                    select(func.max(StudentActivityLog.occurred_at))
                    .where(
                        StudentActivityLog.student_id == student.id,
                        StudentActivityLog.is_deleted == False,
                    )
                )
                log_result = await self.db.execute(log_query)
                log_ts = log_result.scalar()
                if log_ts and (not last_activity or log_ts > last_activity):
                    last_activity = log_ts
            except Exception:
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
