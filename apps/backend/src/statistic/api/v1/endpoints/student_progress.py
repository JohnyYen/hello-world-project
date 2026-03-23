from fastapi import APIRouter, Depends, status
from uuid import UUID

from src.statistic.application.usecase.get_student_progress_usecase import (
    GetStudentProgressUseCase,
)
from src.statistic.api.v1.schemas.student_progress import StudentProgressResponse


router = APIRouter(tags=["Student Progress"])


@router.get(
    "/students/{student_id}/progress",
    response_model=StudentProgressResponse,
    summary="Obtener reporte de progreso por estudiante",
    description="Retorna métricas de progreso, rendimiento por nivel y distribución de actividades",
    status_code=status.HTTP_200_OK,
)
async def get_student_progress(
    student_id: str,
    use_case: GetStudentProgressUseCase = Depends(),
) -> StudentProgressResponse:
    """
    Obtiene el reporte completo de progreso de un estudiante.

    Returns:
        - student_id: UUID del estudiante
        - kpis: Métricas clave (niveles completados, juegos jugados, tiempo, puntuación promedio, racha)
        - progress_over_time: Evolución del progreso en el tiempo
        - level_performance: Rendimiento detallado por nivel
        - activity_distribution: Distribución del tiempo por juego
    """
    return await use_case.execute(student_id)
