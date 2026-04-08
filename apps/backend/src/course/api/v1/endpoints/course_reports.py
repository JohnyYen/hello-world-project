from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.shared.infrastructure.session import get_db
from src.course.infrastructure.course_repository import CourseRepository
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.course.application.usecase.get_course_report_usecase import GetCourseReportUseCase
from src.course.api.v1.schemas import course_report as schemas

router = APIRouter(
    prefix="/courses",
    tags=["Course Reports"],
    dependencies=[Depends(HTTPBearer())],
)


async def get_course_report_usecase(db: AsyncSession = Depends(get_db)) -> GetCourseReportUseCase:
    course_repo = CourseRepository(db)
    progress_repo = ProgressRepository(db)
    return GetCourseReportUseCase(course_repo, progress_repo)


@router.get("/", response_model=List[schemas.CourseResponse])
async def list_courses(
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Lista todos los cursos con conteo de estudiantes inscritos.
    """
    courses = await usecase.execute_list()
    return [schemas.CourseResponse.model_validate(c) for c in courses]


@router.get("/reports/kpis", response_model=schemas.CourseReportKPIsResponse)
async def get_report_kpis(
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Obtiene KPIs generales para reportes de cursos.
    """
    kpis = await usecase.execute_kpis()
    return schemas.CourseReportKPIsResponse.model_validate(kpis)


@router.get("/metrics", response_model=List[schemas.CourseMetricsResponse])
async def get_course_metrics(
    course_ids: str = Query(..., description="Comma-separated course IDs"),
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Obtiene métricas para múltiples cursos.
    """
    ids = [int(x.strip()) for x in course_ids.split(",")]
    metrics = await usecase.execute_metrics(ids)
    return [schemas.CourseMetricsResponse.model_validate(m) for m in metrics]


@router.get("/{course_id}/metrics", response_model=schemas.CourseMetricsResponse)
async def get_course_metrics_single(
    course_id: int,
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Obtiene métricas para un curso específico.
    """
    metrics_list = await usecase.execute_metrics([course_id])
    if not metrics_list:
        raise HTTPException(status_code=404, detail="Course not found or has no metrics")
    return schemas.CourseMetricsResponse.model_validate(metrics_list[0])


@router.get(
    "/{course_id}/progress-over-time",
    response_model=List[schemas.CourseProgressOverTimeResponse],
)
async def get_progress_over_time(
    course_id: int,
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Obtiene el progreso a lo largo del tiempo para un curso.
    """
    return await usecase.execute_progress_over_time(course_id)


@router.get(
    "/{course_id}/activity-summary",
    response_model=List[schemas.StudentActivitySummaryResponse],
)
async def get_activity_summary(
    course_id: int,
    days: int = Query(30, ge=1, le=90),
    usecase: GetCourseReportUseCase = Depends(get_course_report_usecase),
):
    """
    Obtiene resumen de actividad diario para un curso (últimos N días).
    """
    return await usecase.execute_activity_summary(course_id, days)
