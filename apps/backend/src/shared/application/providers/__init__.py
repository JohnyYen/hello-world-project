"""
Shared Application Providers.

This module exports all provider functions for dependency injection across
the Users, Statistic, and Game domains.

Usage:
    from src.shared.application.providers import (
        get_user_service,
        get_student_service,
        # etc.
    )
"""

# Users domain providers
from src.shared.application.providers.users_providers import (
    get_user_repository,
    get_student_repository,
    get_professor_repository,
    get_teacher_settings_repository,
    get_lms_credential_repository,
    get_user_service,
    get_student_service,
    get_professor_service,
    get_teacher_settings_service,
    get_lms_credential_service,
)

# Statistic domain providers
from src.shared.application.providers.statistic_providers import (
    get_xapi_statement_repository,
    get_feedback_repository,
    get_progress_repository,
    get_metric_type_repository,
    get_xapi_statement_service,
    get_feedback_service,
    get_progress_service,
    get_metric_type_service,
)

# Game domain providers
from src.shared.application.providers.game_providers import (
    get_game_repository,
    get_level_repository,
    get_game_instance_repository,
    get_segment_level_repository,
    get_game_service,
    get_level_service,
    get_game_instance_service,
    get_segment_level_service,
)

__all__ = [
    # Users domain - Repositories
    "get_user_repository",
    "get_student_repository",
    "get_professor_repository",
    "get_teacher_settings_repository",
    "get_lms_credential_repository",
    # Users domain - Services
    "get_user_service",
    "get_student_service",
    "get_professor_service",
    "get_teacher_settings_service",
    "get_lms_credential_service",
    # Statistic domain - Repositories
    "get_xapi_statement_repository",
    "get_feedback_repository",
    "get_progress_repository",
    "get_metric_type_repository",
    # Statistic domain - Services
    "get_xapi_statement_service",
    "get_feedback_service",
    "get_progress_service",
    "get_metric_type_service",
    # Game domain - Repositories
    "get_game_repository",
    "get_level_repository",
    "get_game_instance_repository",
    "get_segment_level_repository",
    # Game domain - Services
    "get_game_service",
    "get_level_service",
    "get_game_instance_service",
    "get_segment_level_service",
]
