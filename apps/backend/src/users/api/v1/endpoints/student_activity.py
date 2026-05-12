from uuid import UUID
from fastapi import APIRouter, Depends, Query

from src.users.application.usecase.get_student_activity_usecase import (
    GetStudentActivityUseCase,
)
from src.users.api.v1.schemas.activity_log import (
    HeatMapResponse,
    ActivitySummaryResponse,
)


router = APIRouter(prefix="/students", tags=["Student Activity"])


@router.get("/{student_id}/activity/heatmap", response_model=HeatMapResponse)
async def get_student_activity_heatmap(
    student_id: UUID,
    days: int = Query(default=30, ge=1, le=365),
    use_case: GetStudentActivityUseCase = Depends(),
):
    """
    Obtiene los datos del heatmap de actividad del estudiante.
    """
    return await use_case.get_heatmap_data(str(student_id), days)


@router.get("/{student_id}/activity/summary", response_model=ActivitySummaryResponse)
async def get_student_activity_summary(
    student_id: UUID,
    use_case: GetStudentActivityUseCase = Depends(),
):
    """
    Obtiene el resumen de actividad del estudiante.
    """
    return await use_case.get_activity_summary(str(student_id))