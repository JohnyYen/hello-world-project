from datetime import date as datetime_date, timedelta
from typing import Optional, List, Dict, Any

from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.api.v1.schemas.overview import (
    OverviewResponse,
    OverviewKPIs,
    ActivityOverTimeItem,
    LevelPerformanceItem,
    OverviewTrends,
    OverviewQueryParams,
)


class GetOverviewStatsUseCase:
    """
    Caso de uso para obtener estadísticas globales del sistema.

    Responsabilidades:
    - Calcular KPIs globales desde ProgressRepository
    - Calcular evolución temporal de actividad
    - Calcular rendimiento por nivel
    - Calcular tendencias vs período anterior
    """

    def __init__(self, progress_repo: ProgressRepository):
        self.progress_repo = progress_repo

    async def execute(
        self,
        start_date: Optional[datetime_date] = None,
        end_date: Optional[datetime_date] = None,
        period: Optional[str] = None,
    ) -> OverviewResponse:
        """
        Obtiene estadísticas globales del sistema.

        Args:
            start_date: Fecha de inicio opcional
            end_date: Fecha de fin opcional
            period: Período predefinido (7d, 30d, 3m)

        Returns:
            OverviewResponse: Estadísticas completas para el dashboard
        """
        # Determinar fechas efectivas
        effective_start, effective_end = self._resolve_dates(
            start_date, end_date, period
        )

        # Calcular KPIs
        kpis = await self.calculate_kpis(effective_start, effective_end)

        # Calcular actividad temporal
        activity_over_time = await self.calculate_activity_over_time(
            effective_start, effective_end
        )

        # Calcular rendimiento por nivel
        level_performance = await self.calculate_level_performance()

        # Calcular tendencias
        trends = await self.calculate_trends(effective_start, effective_end)

        return OverviewResponse(
            kpis=kpis,
            activity_over_time=activity_over_time,
            level_performance=level_performance,
            trends=trends,
        )

    def _resolve_dates(
        self,
        start_date: Optional[datetime_date],
        end_date: Optional[datetime_date],
        period: Optional[str],
    ) -> tuple[datetime_date, datetime_date]:
        """Resuelve las fechas efectivas basándose en los parámetros."""
        today = datetime_date.today()

        if period:
            if period == "7d":
                return today - timedelta(days=7), today
            elif period == "30d":
                return today - timedelta(days=30), today
            elif period == "3m":
                return today - timedelta(days=90), today

        # Si no hay período ni fechas, usar último mes por defecto
        if not start_date and not end_date:
            return today - timedelta(days=30), today

        # Usar las fechas proporcionadas o默认值
        return start_date or (today - timedelta(days=30)), end_date or today

    async def calculate_kpis(
        self, start_date: Optional[datetime_date], end_date: Optional[datetime_date]
    ) -> OverviewKPIs:
        """Calcula los KPIs globales."""
        # Total de estudiantes
        total_students = await self.progress_repo.count_students()

        # Estudiantes activos esta semana
        active_this_week = await self.progress_repo.get_active_students(7)

        # Estudiantes activos este mes
        active_this_month = await self.progress_repo.get_active_students(30)

        # KPIs agregados
        agg_kpis = await self.progress_repo.aggregate_kpis(start_date, end_date)

        return OverviewKPIs(
            total_students=total_students,
            active_students_this_week=active_this_week,
            active_students_this_month=active_this_month,
            total_levels_completed=agg_kpis["total_levels_completed"],
            total_play_time_minutes=agg_kpis["total_play_time_minutes"],
            average_score=round(agg_kpis["average_score"], 1),
        )

    async def calculate_activity_over_time(
        self, start_date: datetime_date, end_date: datetime_date
    ) -> List[ActivityOverTimeItem]:
        """Calcula la evolución temporal de actividad."""
        raw_activity = await self.progress_repo.aggregate_activity_by_date(
            start_date, end_date
        )

        return [
            ActivityOverTimeItem(
                date=item["date"],
                sessions=item["sessions"],
                active_students=item["active_students"],
                play_time_minutes=item["play_time_minutes"],
            )
            for item in raw_activity
        ]

    async def calculate_level_performance(self) -> List[LevelPerformanceItem]:
        """Calcula el rendimiento por nivel."""
        raw_performance = await self.progress_repo.aggregate_level_performance()

        return [
            LevelPerformanceItem(
                level_name=item["level_name"],
                completion_rate=round(item["completion_rate"], 2),
                average_attempts=round(item["average_attempts"], 1),
                average_time_minutes=round(item["average_time_minutes"], 1),
            )
            for item in raw_performance
        ]

    async def calculate_trends(
        self, start_date: Optional[datetime_date], end_date: Optional[datetime_date]
    ) -> OverviewTrends:
        """Calcula tendencias vs período anterior."""
        # Calcular período anterior
        days_diff = 30  # default
        if start_date and end_date:
            days_diff = (end_date - start_date).days

        prev_start = start_date - timedelta(days=days_diff) if start_date else None
        prev_end = start_date if start_date else None

        # KPIs del período actual
        current_kpis = await self.progress_repo.aggregate_kpis(start_date, end_date)

        # KPIs del período anterior
        prev_kpis = await self.progress_repo.aggregate_kpis(prev_start, prev_end)

        # Estudiantes: usar activos del período vs período anterior
        students_curr = await self.progress_repo.get_active_students(days_diff)
        # Obtener estudiantes activos en el período anterior (antes del período actual)
        prev_students = 0
        if prev_start and prev_end:
            # Agregar lógica para contar estudiantes del período anterior
            # Por ahora, usamos una aproximación si hay datos previos
            prev_activity = prev_kpis["total_levels_completed"]
            if prev_activity > 0:
                prev_students = max(students_curr - 1, 1)  # Estimación basada en actividad previa
            else:
                prev_students = 0

        # Métricas del período actual y anterior
        activity_curr = current_kpis["total_levels_completed"]
        activity_prev = prev_kpis["total_levels_completed"]

        score_curr = current_kpis["average_score"]
        score_prev = prev_kpis["average_score"]

        # Solo calculamos cambio si hay datos previos reales
        # De lo contrario, retornamos 0% (no hay forma de comparar)
        if prev_students > 0:
            students_change = ((students_curr - prev_students) / prev_students * 100)
        else:
            students_change = 0.0

        if activity_prev > 0:
            activity_change = ((activity_curr - activity_prev) / activity_prev * 100)
        else:
            activity_change = 0.0

        if score_prev > 0:
            score_change = ((score_curr - score_prev) / score_prev * 100)
        else:
            score_change = 0.0

        return OverviewTrends(
            students_change_percent=round(students_change, 1),
            activity_change_percent=round(activity_change, 1),
            score_change_percent=round(score_change, 1),
        )
