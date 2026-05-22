from typing import List, Optional
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, func

from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.student_activity_log import StudentActivityLog


class StudentActivityLogRepository(BaseRepository[StudentActivityLog]):
    """
    Repositorio para el registro de actividad de estudiantes.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, StudentActivityLog)

    async def create_log(
        self,
        student_id: UUID,
        activity_type: str,
        occurred_at: Optional[datetime] = None,
        metadata: Optional[dict] = None,
    ) -> StudentActivityLog:
        """
        Crea un nuevo registro de actividad.

        Args:
            student_id: ID del estudiante
            activity_type: Tipo de actividad (login, game_session, progress_sync, etc.)
            occurred_at: Fecha y hora de la actividad (default: now)
            metadata: Metadatos adicionales en formato JSON

        Returns:
            StudentActivityLog: Nuevo registro creado
        """
        log_data = {
            "student_id": student_id,
            "activity_type": activity_type,
            "occurred_at": occurred_at or datetime.now(timezone.utc),
            "metadata": metadata or {},
        }
        return await self.create(log_data)

    async def get_activity_by_date_range(
        self,
        student_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> List[StudentActivityLog]:
        """
        Obtiene los registros de actividad en un rango de fechas.

        Args:
            student_id: ID del estudiante
            start_date: Fecha de inicio
            end_date: Fecha de fin

        Returns:
            List[StudentActivityLog]: Lista de registros de actividad
        """
        query = (
            select(StudentActivityLog)
            .where(
                and_(
                    StudentActivityLog.student_id == student_id,
                    StudentActivityLog.occurred_at >= start_date,
                    StudentActivityLog.occurred_at <= end_date,
                    StudentActivityLog.is_deleted == False,
                )
            )
            .order_by(StudentActivityLog.occurred_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_activity_by_hour(
        self,
        student_id: UUID,
        days: int = 30,
    ) -> List[StudentActivityLog]:
        """
        Obtiene los registros de actividad de los últimos N días.

        Args:
            student_id: ID del estudiante
            days: Número de días hacia atrás

        Returns:
            List[StudentActivityLog]: Lista de registros de actividad
        """
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return await self.get_activity_by_date_range(student_id, start_date, datetime.now(timezone.utc))

    async def count_by_day_and_hour(
        self,
        student_id: UUID,
        days: int = 30,
    ) -> dict:
        """
        Cuenta la actividad por día y hora para el heatmap.
        Retorna un diccionario con la estructura:
        { "day": { hour: count } }

        Args:
            student_id: ID del estudiante
            days: Número de días hacia atrás

        Returns:
            dict: Diccionario de conteos por día y hora
        """
        activities = await self.get_activity_by_hour(student_id, days)
        
        # Inicializar estructura
        result = {}
        day_names = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        
        for day in day_names:
            result[day] = {hour: 0 for hour in range(24)}
        
        for activity in activities:
            if activity.occurred_at:
                # Get day name (weekday returns 0=Monday, 6=Sunday)
                day_idx = activity.occurred_at.weekday()
                day_name = day_names[day_idx]
                hour = activity.occurred_at.hour
                result[day_name][hour] += 1
        
        return result