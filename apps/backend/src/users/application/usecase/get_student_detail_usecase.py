from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.domain.student_activity_log import StudentActivityLog
from src.users.infrastructure.user_repository import UserRepository
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.infrastructure.xapi_statement_repository import XAPIStatementRepository
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

        # Buscar usuario (con student eager loaded)
        user_repo = UserRepository(self.db)
        user = await user_repo.get_by_id_with_role(student_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        # Verificar que sea estudiante
        if not user.role or user.role.role_name != "student":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario no es un estudiante",
            )

        # Resolver students.id (tablas como game_instances, progresses, xapi_statements
        # referencian students.id, NO users.id)
        student_record = user.student  # eager loaded via selectinload
        student_db_id = student_record.id if student_record else None

        # Calcular last_activity desde fuentes de actividad REAL del estudiante.
        # Excluimos game_instances porque se crean automáticamente al asignar un juego
        # y NO representan interacción real del estudiante.
        last_activity = None

        # 1. progresses.updated_at (FK a students.id) — xAPI pipeline
        if student_db_id:
            try:
                progress_repo = ProgressRepository(self.db)
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
        #    Cada interacción del videojuego genera un statement xAPI con timestamp
        if student_db_id:
            try:
                xapi_repo = XAPIStatementRepository(self.db)
                xapi_records = await xapi_repo.get_by_student_id(
                    student_db_id, skip=0, limit=1
                )
                if xapi_records:
                    xapi_ts = xapi_records[0].timestamp
                    if xapi_ts and (not last_activity or xapi_ts > last_activity):
                        last_activity = xapi_ts
            except Exception:
                pass

        # 4. student_activity_log.occurred_at (FK a users.id) — log de actividad
        try:
            log_query = (
                select(func.max(StudentActivityLog.occurred_at))
                .where(
                    StudentActivityLog.student_id == user.id,
                    StudentActivityLog.is_deleted == False,
                )
            )
            log_result = await self.db.execute(log_query)
            log_ts = log_result.scalar()
            if log_ts and (not last_activity or log_ts > last_activity):
                last_activity = log_ts
        except Exception:
            pass

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
            last_activity=last_activity,
        )
