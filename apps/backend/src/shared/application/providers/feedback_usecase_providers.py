"""
Provider functions for Feedback UseCases.

This module is separated from `statistic_providers.py` to avoid a circular
import: the UseCase modules import `get_feedback_service` from
`statistic_providers`, so we must NOT import the UseCases from
`statistic_providers`. Instead, the UseCase providers live here and are
imported on demand by the FastAPI endpoints.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.shared.application.providers.statistic_providers import get_feedback_service
from src.statistic.application.service.feedback_service import FeedbackService
from src.statistic.application.usecase.create_feedback_usecase import (
    CreateFeedbackUseCase,
)
from src.statistic.application.usecase.list_feedback_usecase import (
    ListFeedbackUseCase,
)
from src.users.domain.user import User


def get_create_feedback_usecase(
    db: Annotated[AsyncSession, Depends(get_db)],
    feedback_service: Annotated[FeedbackService, Depends(get_feedback_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CreateFeedbackUseCase:
    """Provider for CreateFeedbackUseCase.

    The UseCase's __init__ declares its dependencies via Annotated Depends(),
    so we forward them here for FastAPI to resolve.
    """
    return CreateFeedbackUseCase(
        db=db,
        feedback_service=feedback_service,
        current_user=current_user,
    )


def get_list_feedback_usecase(
    db: Annotated[AsyncSession, Depends(get_db)],
    feedback_service: Annotated[FeedbackService, Depends(get_feedback_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ListFeedbackUseCase:
    """Provider for ListFeedbackUseCase.

    The UseCase's __init__ declares its dependencies via Annotated Depends(),
    so we forward them here for FastAPI to resolve.
    """
    return ListFeedbackUseCase(
        db=db,
        feedback_service=feedback_service,
        current_user=current_user,
    )
