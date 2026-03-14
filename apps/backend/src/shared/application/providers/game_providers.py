"""
Provider functions for Game domain services and repositories.

This module provides FastAPI dependency injection functions for:
- GameRepository
- LevelRepository
- GameInstanceRepository
- SegmentLevelRepository
- GameService
- LevelService
- GameInstanceService
- SegmentLevelService
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db

# Repository imports
from src.game.infrastructure.game_repository import GameRepository
from src.game.infrastructure.level_repository import LevelRepository
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.infrastructure.segment_level_repository import SegmentLevelRepository

# Service imports
from src.game.application.service.game_service import GameService
from src.game.application.service.level_service import LevelService
from src.game.application.service.game_instance_service import GameInstanceService
from src.game.application.service.segment_level_service import SegmentLevelService

# Domain model imports
from src.game.domain.game import Game
from src.game.domain.level import Level
from src.game.domain.game_instance import GameInstance
from src.game.domain.segment_level import SegmentLevel


# ====================
# Repository Providers
# ====================


def get_game_repository(
    db: AsyncSession = Depends(get_db),
) -> GameRepository:
    """Provider for GameRepository."""
    return GameRepository(db)


def get_level_repository(
    db: AsyncSession = Depends(get_db),
) -> LevelRepository:
    """Provider for LevelRepository."""
    return LevelRepository(db)


def get_game_instance_repository(
    db: AsyncSession = Depends(get_db),
) -> GameInstanceRepository:
    """Provider for GameInstanceRepository."""
    return GameInstanceRepository(db)


def get_segment_level_repository(
    db: AsyncSession = Depends(get_db),
) -> SegmentLevelRepository:
    """Provider for SegmentLevelRepository."""
    return SegmentLevelRepository(db)


# ====================
# Service Providers
# ====================


def get_game_service(
    game_repository: Annotated[GameRepository, Depends(get_game_repository)],
) -> GameService:
    """Provider for GameService with injected repository."""
    return GameService(repository=game_repository, model=Game)


def get_level_service(
    level_repository: Annotated[LevelRepository, Depends(get_level_repository)],
) -> LevelService:
    """Provider for LevelService with injected repository."""
    return LevelService(repository=level_repository, model=Level)


def get_game_instance_service(
    game_instance_repository: Annotated[
        GameInstanceRepository, Depends(get_game_instance_repository)
    ],
) -> GameInstanceService:
    """Provider for GameInstanceService with injected repository."""
    return GameInstanceService(repository=game_instance_repository, model=GameInstance)


def get_segment_level_service(
    segment_level_repository: Annotated[
        SegmentLevelRepository, Depends(get_segment_level_repository)
    ],
) -> SegmentLevelService:
    """Provider for SegmentLevelService with injected repository."""
    return SegmentLevelService(repository=segment_level_repository, model=SegmentLevel)
