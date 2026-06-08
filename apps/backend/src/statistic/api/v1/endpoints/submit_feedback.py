from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.shared.application.providers.feedback_usecase_providers import (
    get_create_feedback_usecase,
    get_list_feedback_usecase,
)
from src.statistic.api.v1.schemas.feedback import (
    FeedbackCreate,
    FeedbackListResponse,
    FeedbackSchema,
)
from src.statistic.application.usecase.create_feedback_usecase import (
    CreateFeedbackUseCase,
)
from src.statistic.application.usecase.list_feedback_usecase import (
    ListFeedbackUseCase,
)


router = APIRouter(prefix="/feedback")


@router.post("", response_model=FeedbackSchema, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback: FeedbackCreate,
    usecase: CreateFeedbackUseCase = Depends(get_create_feedback_usecase),
):
    """
    Enviar retroalimentación de un estudiante.
    """
    return await usecase.execute(feedback)


@router.get("/course/{course_id}", response_model=FeedbackListResponse)
async def get_course_feedback(
    course_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    usecase: ListFeedbackUseCase = Depends(get_list_feedback_usecase),
):
    """
    Obtener feedback de todos los estudiantes en un curso.
    """
    return await usecase.execute_by_course(course_id=course_id, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=FeedbackListResponse)
async def get_student_feedback_history(
    student_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    usecase: ListFeedbackUseCase = Depends(get_list_feedback_usecase),
):
    """
    Obtener feedback histórico del estudiante.
    """
    return await usecase.execute(student_id=student_id, skip=skip, limit=limit)
