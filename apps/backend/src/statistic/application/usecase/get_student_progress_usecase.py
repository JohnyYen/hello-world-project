from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

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
    - Consultar datos de progreso desde la tabla progresses (dominio statistic)
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
            StudentProgressResponse: Datos de progreso para el frontend

        Raises:
            HTTPException 404: Si no se encuentra el progreso
        """
        try:
            student_uuid = UUID(student_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de estudiante inválido",
            )

        progress_repo = ProgressRepository(self.db)
        progresses = await progress_repo.get_by_student_id(student_uuid)

        if not progresses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró progreso para este estudiante",
            )

        kpis = self._calculate_kpis(progresses)
        progress_over_time = self._calculate_progress_over_time(progresses)
        level_performance = self._calculate_level_performance(progresses)
        activity_distribution = self._calculate_activity_distribution(progresses)

        return StudentProgressResponse(
            student_id=student_id,
            kpis=kpis,
            progress_over_time=progress_over_time,
            level_performance=level_performance,
            activity_distribution=activity_distribution,
        )

    def _calculate_kpis(self, progresses: list) -> StudentReportKPIs:
        completed = [p for p in progresses if p.objectives_completed > 0]
        unique_games = set()
        total_time = 0
        total_score = 0
        last_activity = None

        for p in progresses:
            if p.segment_level_id:
                unique_games.add(str(p.segment_level_id))
            total_time += p.attempt_count * 5
            if p.efficiency_rating > 0:
                total_score += p.efficiency_rating
            if p.updated_at and (not last_activity or p.updated_at > last_activity):
                last_activity = p.updated_at

        avg_score = total_score / len(progresses) if progresses else 0.0

        return StudentReportKPIs(
            total_levels_completed=len(completed),
            total_games_played=len(unique_games),
            total_play_time=total_time,
            average_score=round(avg_score, 1),
            current_streak=len(completed),
            last_activity=last_activity,
        )

    def _calculate_progress_over_time(
        self, progresses: list
    ) -> list[ProgressOverTimeItem]:
        sorted_progress = sorted(
            [p for p in progresses if p.created_at is not None],
            key=lambda p: p.created_at
        )
        result = []
        for p in sorted_progress[:10]:
            result.append(
                ProgressOverTimeItem(
                    date=p.created_at.strftime("%b %d") if p.created_at else "N/A",
                    level=p.attempt_count,
                    score=p.efficiency_rating,
                    time_spent=p.attempt_count * 5,
                )
            )
        return result

    def _calculate_level_performance(
        self, progresses: list
    ) -> list[LevelPerformanceItem]:
        result = []
        for p in progresses[:6]:
            result.append(
                LevelPerformanceItem(
                    level_name=f"Nivel {p.attempt_count}",
                    score=p.efficiency_rating,
                    attempts=p.attempt_count + 1,
                    time_spent=p.attempt_count * 5,
                    completed=p.objectives_completed > 0,
                )
            )
        return result

    def _calculate_activity_distribution(
        self, progresses: list
    ) -> list[ActivityDistributionItem]:
        game_times: dict[str, int] = {}
        game_sessions: dict[str, int] = {}

        for p in progresses:
            # Skip if segment_level_id is None
            if p.segment_level_id is None:
                continue
            game_key = str(p.segment_level_id)[:8]
            game_times[game_key] = game_times.get(game_key, 0) + (p.attempt_count * 5)
            game_sessions[game_key] = game_sessions.get(game_key, 0) + 1

        result = []
        for game_key in list(game_times.keys())[:4]:
            result.append(
                ActivityDistributionItem(
                    game_name=f"Juego {game_key}",
                    time_spent=game_times[game_key],
                    sessions=game_sessions[game_key],
                )
            )
        return result
