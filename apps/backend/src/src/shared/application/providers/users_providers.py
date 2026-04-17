"""
Provider functions for Users domain services and repositories.

This module provides FastAPI dependency injection functions for:
- UserRepository
- StudentRepository
- ProfessorRepository
- TeacherSettingsRepository
- LMSCredentialRepository
- UserService
- StudentService
- ProfessorService
- TeacherSettingsService
- LMSCredentialService
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db

# Repository imports
from src.users.infrastructure.user_repository import UserRepository
from src.users.infrastructure.student_repository import StudentRepository
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.infrastructure.teacher_settings_repository import (
    TeacherSettingsRepository,
)
from src.users.infrastructure.lms_credential_repository import LMSCredentialRepository

# Service imports
from src.users.application.service.user_service import UserService
from src.users.application.service.student_service import StudentService
from src.users.application.service.professor_service import ProfessorService
from src.users.application.service.teacher_settings_service import (
    TeacherSettingsService,
)
from src.users.application.service.lms_credential_service import LMSCredentialService

# Domain model imports
from src.users.domain.user import User
from src.users.domain.student import Student
from src.users.domain.professor import Professor
from src.users.domain.teacher_settings import TeacherSettings
from src.users.domain.lms_credential import LMSCredential


# ====================
# Repository Providers
# ====================


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Provider for UserRepository."""
    return UserRepository(db)


def get_student_repository(
    db: AsyncSession = Depends(get_db),
) -> StudentRepository:
    """Provider for StudentRepository."""
    return StudentRepository(db)


def get_professor_repository(
    db: AsyncSession = Depends(get_db),
) -> ProfessorRepository:
    """Provider for ProfessorRepository."""
    return ProfessorRepository(db)


def get_teacher_settings_repository(
    db: AsyncSession = Depends(get_db),
) -> TeacherSettingsRepository:
    """Provider for TeacherSettingsRepository."""
    return TeacherSettingsRepository(db)


def get_lms_credential_repository(
    db: AsyncSession = Depends(get_db),
) -> LMSCredentialRepository:
    """Provider for LMSCredentialRepository."""
    return LMSCredentialRepository(db)


# ====================
# Service Providers
# ====================


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Provider for UserService with injected repository."""
    return UserService(repository=user_repository, model=User)


def get_student_service(
    student_repository: Annotated[StudentRepository, Depends(get_student_repository)],
) -> StudentService:
    """Provider for StudentService with injected repository."""
    return StudentService(repository=student_repository, model=Student)


def get_professor_service(
    professor_repository: Annotated[
        ProfessorRepository, Depends(get_professor_repository)
    ],
) -> ProfessorService:
    """Provider for ProfessorService with injected repository."""
    return ProfessorService(repository=professor_repository, model=Professor)


def get_teacher_settings_service(
    teacher_settings_repository: Annotated[
        TeacherSettingsRepository, Depends(get_teacher_settings_repository)
    ],
) -> TeacherSettingsService:
    """Provider for TeacherSettingsService with injected repository."""
    return TeacherSettingsService(
        repository=teacher_settings_repository, model=TeacherSettings
    )


def get_lms_credential_service(
    lms_credential_repository: Annotated[
        LMSCredentialRepository, Depends(get_lms_credential_repository)
    ],
) -> LMSCredentialService:
    """Provider for LMSCredentialService with injected repository."""
    return LMSCredentialService(
        repository=lms_credential_repository, model=LMSCredential
    )
