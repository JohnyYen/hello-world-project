from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.users.infrastructure.student_activity_log_repository import StudentActivityLogRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.users.api.v1.schemas.activity_log import (
    HeatMapResponse,
    HeatMapDataPoint,
    ActivitySummaryResponse,
)


class GetStudentActivityUseCase:
    """
    Caso de uso para obtener datos de actividad del estudiante.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_heatmap_data(
        self, student_id: str, days: int = 30
    ) -> HeatMapResponse:
        """
        Obtiene los datos del heatmap de actividad.

        Args:
            student_id: UUID del estudiante
            days: Número de días hacia atrás (default 30)

        Returns:
            HeatMapResponse: Datos del heatmap
        """
        try:
            student_uuid = UUID(student_id)
        except ValueError:
            raise ValueError("ID de estudiante inválido")

        log_repo = StudentActivityLogRepository(self.db)
        activity_counts = await log_repo.count_by_day_and_hour(student_uuid, days)

        # Convertir a formato de respuesta
        data_points: List[HeatMapDataPoint] = []
        total_activities = 0

        day_names = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        for day in day_names:
            for hour in range(24):
                value = activity_counts.get(day, {}).get(hour, 0)
                data_points.append(
                    HeatMapDataPoint(day=day, hour=hour, value=value)
                )
                total_activities += value

        return HeatMapResponse(
            student_id=student_id,
            days=days,
            data=data_points,
            total_activities=total_activities,
        )

    async def get_activity_summary(self, student_id: str) -> ActivitySummaryResponse:
        """
        Obtiene un resumen de la actividad del estudiante.

        Args:
            student_id: UUID del estudiante

        Returns:
            ActivitySummaryResponse: Resumen de actividad
        """
        try:
            student_uuid = UUID(student_id)
        except ValueError:
            raise ValueError("ID de estudiante inválido")

        log_repo = StudentActivityLogRepository(self.db)
        
        # Obtener actividades de los últimos 30 días
        activities = await log_repo.get_activity_by_hour(student_uuid, 30)
        
        # Calcular última actividad
        last_active = activities[0].occurred_at if activities else None
        
        # Calcular racha (días consecutivos con actividad)
        current_streak = self._calculate_streak(activities)
        
        # Verificar si está activo hoy
        today = datetime.utcnow().date()
        active_today = any(
            a.occurred_at.date() == today 
            for a in activities 
            if a.occurred_at
        )
        
        return ActivitySummaryResponse(
            student_id=student_id,
            last_active_at=last_active,
            total_sessions=len(activities),
            current_streak=current_streak,
            active_today=active_today,
        )

    def _calculate_streak(self, activities: list) -> int:
        """Calcula la racha de días consecutivos con actividad"""
        if not activities:
            return 0

        # Obtener fechas únicas de actividad
        activity_dates = set()
        for a in activities:
            if a.occurred_at:
                activity_dates.add(a.occurred_at.date())

        if not activity_dates:
            return 0

        # Ordenar fechas
        sorted_dates = sorted(activity_dates, reverse=True)
        
        # Contar días consecutivos desde hoy
        streak = 0
        today = datetime.utcnow().date()
        
        # Empezar desde hoy o yesterday
        check_date = today
        if today not in activity_dates:
            check_date = today - timedelta(days=1)
            if check_date not in activity_dates:
                return 0

        while check_date in activity_dates:
            streak += 1
            check_date -= timedelta(days=1)

        return streak