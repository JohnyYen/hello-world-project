"""
Tests: AssignGameToCourseUseCase
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.course.application.usecase.assign_game_to_course_usecase import AssignGameToCourseUseCase
from src.course.domain.game_assignment_exceptions import GameAlreadyAssignedException, GameNotFoundException
from src.shared.domain.exceptions import NotFoundException


@pytest.fixture
def sample_course_id():
    return uuid4()


@pytest.fixture
def sample_game_id():
    return uuid4()


@pytest.fixture
def sample_course(sample_course_id, sample_game_id):
    course = MagicMock()
    course.id = sample_course_id
    course.name = "Matemáticas 2025"
    course.game_id = None  # sin juego asignado
    course.deleted_at = None
    return course


@pytest.fixture
def assigned_course(sample_course_id, sample_game_id):
    course = MagicMock()
    course.id = sample_course_id
    course.name = "Matemáticas 2025"
    course.game_id = sample_game_id  # YA tiene juego asignado
    course.deleted_at = None
    return course


@pytest.fixture
def sample_game(sample_game_id):
    game = MagicMock()
    game.id = sample_game_id
    game.title = "Juego Matemáticas"
    game.deleted_at = None
    return game


class TestAssignGameToCourseUseCase:
    @pytest.mark.asyncio
    async def test_assign_game_to_course_success(
        self, mock_db, sample_course_id, sample_game_id, sample_course, sample_game
    ):
        """Asigna juego a curso sin juego previo y retorna detalle del curso."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)
        mock_course_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_course_repo.get_professors_for_course = AsyncMock(return_value=[])

        mock_game_repo = MagicMock()
        mock_game_repo.get_by_id = AsyncMock(return_value=sample_game)

        uc = AssignGameToCourseUseCase.__new__(AssignGameToCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo
        uc.game_repo = mock_game_repo

        # After assignment, game_id should be set
        sample_course.game_id = sample_game_id
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        result = await uc.execute(sample_course_id, sample_game_id)

        assert result is not None
        mock_game_repo.get_by_id.assert_awaited_once_with(sample_game_id, include_deleted=False)
        mock_db.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_assign_game_to_course_already_assigned_raises(
        self, mock_db, sample_course_id, sample_game_id, assigned_course
    ):
        """Si el curso ya tiene juego asignado, lanza GameAlreadyAssignedException."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(return_value=assigned_course)
        uc = AssignGameToCourseUseCase.__new__(AssignGameToCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo
        uc.game_repo = MagicMock()

        with pytest.raises(GameAlreadyAssignedException):
            await uc.execute(sample_course_id, sample_game_id)

        # No se debe consultar el juego si el curso ya tiene juego
        uc.game_repo.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_assign_nonexistent_game_raises(
        self, mock_db, sample_course_id, sample_game_id, sample_course
    ):
        """Si el juego no existe, lanza GameNotFoundException."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)

        mock_game_repo = MagicMock()
        mock_game_repo.get_by_id = AsyncMock(return_value=None)

        uc = AssignGameToCourseUseCase.__new__(AssignGameToCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo
        uc.game_repo = mock_game_repo

        with pytest.raises(GameNotFoundException):
            await uc.execute(sample_course_id, sample_game_id)

    @pytest.mark.asyncio
    async def test_assign_game_nonexistent_course_raises(
        self, mock_db, sample_course_id, sample_game_id
    ):
        """Si el curso no existe, lanza NotFoundException."""
        mock_course_repo = MagicMock()
        mock_course_repo.get_by_id_with_relations = AsyncMock(return_value=None)

        uc = AssignGameToCourseUseCase.__new__(AssignGameToCourseUseCase)
        uc.db = mock_db
        uc.course_repo = mock_course_repo
        uc.game_repo = MagicMock()

        with pytest.raises(NotFoundException):
            await uc.execute(sample_course_id, sample_game_id)
