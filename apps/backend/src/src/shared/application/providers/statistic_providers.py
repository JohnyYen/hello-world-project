"""
Provider functions for Statistic domain services and repositories.

This module provides FastAPI dependency injection functions for:
- XAPIStatementRepository
- FeedbackRepository
- ProgressRepository
- MetricTypeRepository
- XAPIStatementService
- FeedbackService
- ProgressService
- MetricTypeService
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db

# Repository imports
from src.statistic.infrastructure.xapi_statement_repository import (
    XAPIStatementRepository,
)
from src.statistic.infrastructure.feedback_repository import FeedbackRepository
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.infrastructure.metric_type_repository import MetricTypeRepository

# Service imports
from src.statistic.application.service.xapi_statement_service import (
    XAPIStatementService,
)
from src.statistic.application.service.feedback_service import FeedbackService
from src.statistic.application.service.progress_service import ProgressService
from src.statistic.application.service.metric_type_service import MetricTypeService

# Domain model imports
from src.statistic.domain.xapi_statement import XAPIStatement
from src.statistic.domain.feedback import Feedback
from src.statistic.domain.progress import Progress
from src.statistic.domain.metric_type import MetricType


# ====================
# Repository Providers
# ====================


def get_xapi_statement_repository(
    db: AsyncSession = Depends(get_db),
) -> XAPIStatementRepository:
    """Provider for XAPIStatementRepository."""
    return XAPIStatementRepository(db)


def get_feedback_repository(
    db: AsyncSession = Depends(get_db),
) -> FeedbackRepository:
    """Provider for FeedbackRepository."""
    return FeedbackRepository(db)


def get_progress_repository(
    db: AsyncSession = Depends(get_db),
) -> ProgressRepository:
    """Provider for ProgressRepository."""
    return ProgressRepository(db)


def get_metric_type_repository(
    db: AsyncSession = Depends(get_db),
) -> MetricTypeRepository:
    """Provider for MetricTypeRepository."""
    return MetricTypeRepository(db)


# ====================
# Service Providers
# ====================


def get_xapi_statement_service(
    xapi_statement_repository: Annotated[
        XAPIStatementRepository, Depends(get_xapi_statement_repository)
    ],
) -> XAPIStatementService:
    """Provider for XAPIStatementService with injected repository."""
    # Note: XAPIStatementService currently has custom implementation that uses both
    # db and repository. After migration in Phase 3, it should accept only repository.
    return XAPIStatementService(repository=xapi_statement_repository)


def get_feedback_service(
    feedback_repository: Annotated[
        FeedbackRepository, Depends(get_feedback_repository)
    ],
) -> FeedbackService:
    """Provider for FeedbackService with injected repository."""
    return FeedbackService(repository=feedback_repository, model=Feedback)


def get_progress_service(
    progress_repository: Annotated[
        ProgressRepository, Depends(get_progress_repository)
    ],
) -> ProgressService:
    """Provider for ProgressService with injected repository."""
    return ProgressService(repository=progress_repository, model=Progress)


def get_metric_type_service(
    metric_type_repository: Annotated[
        MetricTypeRepository, Depends(get_metric_type_repository)
    ],
) -> MetricTypeService:
    """Provider for MetricTypeService with injected repository."""
    return MetricTypeService(repository=metric_type_repository, model=MetricType)
