from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.statistic.api.v1.schemas.feedback import FeedbackCreate, FeedbackSchema
from src.statistic.application.service.feedback_service import FeedbackService
from src.shared.infrastructure.session import get_db


router = APIRouter(prefix="/feedback")


@router.post("", response_model=FeedbackSchema, status_code=status.HTTP_201_CREATED)
async def submit_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """
    Enviar retroalimentación de un estudiante.
    """
    service = FeedbackService(db=db)

    # Validate rating is between 1 and 5 if provided
    if feedback.rating is not None and (feedback.rating < 1 or feedback.rating > 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5",
        )

    # Create feedback using the service
    created_feedback = await service.create(feedback.model_dump())

    return created_feedback


@router.get("/{student_id}", response_model=List[FeedbackSchema])
async def get_student_feedback_history(
    student_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Obtener feedback histórico del estudiante.
    """
    service = FeedbackService(db=db)

    # Get feedback by student_id
    feedbacks = await service.repository.get_by_student_id(
        student_id=student_id, include_deleted=False
    )

    # Apply pagination manually since get_by_student_id returns a list
    return feedbacks[skip : skip + limit]
