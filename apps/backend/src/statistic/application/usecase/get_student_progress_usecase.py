from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date as datetime_date, timedelta
from collections import defaultdict

from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.api.v1.schemas.student_progress import (
    StudentProgressResponse,
    StudentReportKPIs,
    ProgressOverTimeItem,
    LevelPerformanceItem,
    ActivityDistributionItem,
)


class GetStudentProgressUseCase:
    """
    Caso de uso para obtener el progreso de un estudiante desde el dominio statistic.

    Responsabilidades:
    - Consultar datos de progreso enriquecidos (con nombres de nivel y juego)
    - Calcular métricas: KPIs, progreso en el tiempo, rendimiento por nivel, distribución de actividades
    - Retornar estructura lista para el frontend
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def execute(self, student_id: str) -> StudentProgressResponse:
        """
        Obtiene el reporte de progreso de un estudiante.

        Args:
            student_id: UUID del estudiante

        Returns:
            StudentProgressResponse: Datos de progreso para el frontend (puede estar vacío si no hay datos)

        Raises:
            HTTPException 400: Si el ID de estudiante no es un UUID válido
        """
        try:
            student_uuid = UUID(student_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de estudiante inválido",
            )

        progress_repo = ProgressRepository(self.db)
        enriched_rows = await progress_repo.get_enriched_by_student_id(student_uuid)

        # Si no hay progreso, retornar datos vacíos (no es un error)
        if not enriched_rows:
            return StudentProgressResponse(
                student_id=student_id,
                kpis=StudentReportKPIs(
                    total_levels_completed=0,
                    total_games_played=0,
                    total_play_time=0,
                    average_score=0.0,
                    current_streak=0,
                    last_activity=None,
                ),
                progress_over_time=[],
                level_performance=[],
                activity_distribution=[],
            )

        kpis = self._calculate_kpis(enriched_rows)
        progress_over_time = self._calculate_progress_over_time(enriched_rows)
        level_performance = self._calculate_level_performance(enriched_rows)
        activity_distribution = self._calculate_activity_distribution(enriched_rows)

        return StudentProgressResponse(
            student_id=student_id,
            kpis=kpis,
            progress_over_time=progress_over_time,
            level_performance=level_performance,
            activity_distribution=activity_distribution,
        )

    def _calculate_kpis(self, enriched_rows: list) -> StudentReportKPIs:
        """Calcula KPIs del estudiante a partir de datos enriquecidos."""
        completed = [r for r in enriched_rows if r["progress"].objectives_completed > 0]
        unique_games = set()
        total_attempts = 0
        total_score = 0
        last_activity = None
        activity_dates = set()

        for r in enriched_rows:
            p = r["progress"]
            unique_games.add(r["game_title"])
            total_attempts += p.attempt_count
            if p.efficiency_rating > 0:
                total_score += p.efficiency_rating
            if p.created_at:
                activity_dates.add(p.created_at.date())
            if p.updated_at and (not last_activity or p.updated_at > last_activity):
                last_activity = p.updated_at

        avg_score = total_score / len(enriched_rows) if enriched_rows else 0.0

        # Calcular racha actual: días consecutivos hacia atrás desde la última actividad
        current_streak = self._calculate_current_streak(activity_dates)

        return StudentReportKPIs(
            total_levels_completed=len(completed),
            total_games_played=len(unique_games),
            total_play_time=total_attempts,
            average_score=round(avg_score, 1),
            current_streak=current_streak,
            last_activity=last_activity,
        )

    def _calculate_current_streak(self, activity_dates: set) -> int:
        """
        Calcula la racha actual de días consecutivos de actividad.

        Cuenta hacia atrás desde la última fecha de actividad hasta
        encontrar un día sin actividad.
        """
        if not activity_dates:
            return 0

        sorted_dates = sorted(activity_dates, reverse=True)
        streak = 1  # Al menos 1 día si hay actividad

        for i in range(len(sorted_dates) - 1):
            diff = (sorted_dates[i] - sorted_dates[i + 1]).days
            if diff == 1:
                streak += 1
            elif diff > 1:
                break  # Se rompió la racha

        return streak

    def _calculate_progress_over_time(
        self, enriched_rows: list
    ) -> list[ProgressOverTimeItem]:
        """Calcula evolución del progreso con nombres de nivel reales."""
        sorted_data = sorted(
            [r for r in enriched_rows if r["progress"].created_at is not None],
            key=lambda r: r["progress"].created_at,
        )

        return [
            ProgressOverTimeItem(
                date=p["progress"].created_at.strftime("%b %d"),
                level=p["level_number"],
                score=p["progress"].efficiency_rating,
                time_spent=p["progress"].attempt_count,
            )
            for p in sorted_data
        ]

    def _calculate_level_performance(
        self, enriched_rows: list
    ) -> list[LevelPerformanceItem]:
        """Calcula rendimiento por nivel con nombres reales."""
        # Agrupar por nivel para consolidar múltiples intentos
        level_groups: dict[str, dict] = {}
        for r in enriched_rows:
            p = r["progress"]
            level_name = r["level_title"]
            if level_name not in level_groups:
                level_groups[level_name] = {
                    "total_score": 0,
                    "total_attempts": 0,
                    "total_time": 0,
                    "count": 0,
                    "completed": False,
                }
            lg = level_groups[level_name]
            lg["total_score"] += p.efficiency_rating
            lg["total_attempts"] += p.attempt_count
            lg["total_time"] += p.attempt_count
            lg["count"] += 1
            if p.objectives_completed > 0:
                lg["completed"] = True

        return [
            LevelPerformanceItem(
                level_name=level_name,
                score=round(metrics["total_score"] / metrics["count"], 1),
                attempts=metrics["total_attempts"],
                time_spent=metrics["total_time"],
                completed=metrics["completed"],
            )
            for level_name, metrics in level_groups.items()
        ]

    def _calculate_activity_distribution(
        self, enriched_rows: list
    ) -> list[ActivityDistributionItem]:
        """Calcula distribución de actividad por juego con nombres reales."""
        game_data: dict[str, dict] = defaultdict(
            lambda: {"time_spent": 0, "sessions": 0}
        )

        for r in enriched_rows:
            p = r["progress"]
            game_name = r["game_title"]
            game_data[game_name]["time_spent"] += p.attempt_count
            game_data[game_name]["sessions"] += 1

        return [
            ActivityDistributionItem(
                game_name=game_name,
                time_spent=data["time_spent"],
                sessions=data["sessions"],
            )
            for game_name, data in game_data.items()
        ]
