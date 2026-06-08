"""
Tests: RemoveGameFromCourseUseCase
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.course.application.usecase.remove_game_from_course_usecase import RemoveGameFromCourseUseCase
from src.course.domain.game_assignment_exceptions import GameHasActiveInstancesException
from src.shared.domain.exceptions import NotFoundException


@pytest.fixture
def sample_course_id():
    return uuid4()


@pytest.fixture
def sample_course_no_game(sample_course_id):
    """Curso sin juego asignado."""
    course = MagicMock()
    course.id = sample_course_id
    course.name = "Matemáticas 2025"
    course.game_id = None
    course.deleted_at = None
    return course


@pytest.fixture
def sample_course_with_game(sample_course_id):
    """Curso con juego asignado y sin instancias activas."""
    course = MagicMock()
    course.id = sample_course_id
    course.name = "Matemáticas 2025"
    course.game_id = uuid4()
    course.deleted_at = None
    return course


class TestRemoveGameFromCourseUseCase:
    @pytest.mark.asyncio
    async def test_remove_game_when_no_game_assigned_is_idempotent(
        self, mock_db, sample_course_id, sample_course_no_game
    ):
        """Si el curso no tiene juego asignado, retorna el curso tal cual (idempotent)."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(
            return_value=sample_course_no_game
        )
        mock_course_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_course_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = RemoveGameFromCourseUseCase.__new__(RemoveGameFromCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo

        result = await uc.execute(sample_course_id)

        assert result is not None
        mock_course_repo.has_active_game_instances.assert_not_called()
        mock_db.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_game_success_when_no_active_instances(
        self, mock_db, sample_course_id, sample_course_with_game
    ):
        """Si el curso tiene juego pero sin instancias activas, lo desasigna."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(
            return_value=sample_course_with_game
        )
        mock_course_repo.has_active_game_instances = AsyncMock(return_value=False)
        mock_course_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_course_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = RemoveGameFromCourseUseCase.__new__(RemoveGameFromCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo

        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        sample_course_with_game.game_id = None  # Simula la desasignación

        result = await uc.execute(sample_course_id)

        assert result is not None
        mock_course_repo.has_active_game_instances.assert_awaited_once_with(
            sample_course_id
        )
        mock_db.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_remove_game_raises_when_active_instances_exist(
        self, mock_db, sample_course_id, sample_course_with_game
    ):
        """Si el curso tiene juego e instancias activas, lanza GameHasActiveInstancesException."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(
            return_value=sample_course_with_game
        )
        mock_course_repo.has_active_game_instances = AsyncMock(return_value=True)

        uc = RemoveGameFromCourseUseCase.__new__(RemoveGameFromCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo

        with pytest.raises(GameHasActiveInstancesException):
            await uc.execute(sample_course_id)

        mock_db.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_game_nonexistent_course_raises(
        self, mock_db, sample_course_id
    ):
        """Si el curso no existe, lanza NotFoundException."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(return_value=None)

        uc = RemoveGameFromCourseUseCase.__new__(RemoveGameFromCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo

        with pytest.raises(NotFoundException):
            await uc.execute(sample_course_id)
