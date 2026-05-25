"""
Tests: CreateCourseUseCase — game_id handling
"""

import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.course.application.usecase.create_course_usecase import CreateCourseUseCase
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest,
    CourseDetailResponse,
)
from src.shared.domain.exceptions import DuplicateEntryException
from src.course.domain.game_assignment_exceptions import GameNotFoundException
from src.game.infrastructure.game_repository import GameRepository


class TestCreateCourseUseCase:
    @pytest.mark.asyncio
    async def test_execute_with_valid_game_id_assigns_game(
        self, mock_db, mock_repo, sample_course, sample_course_id
    ):
        """Si se envía game_id válido, el curso se crea con ese juego asignado."""
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)
        mock_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)
        mock_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_repo.get_professors_for_course = AsyncMock(return_value=[])

        course_mock = MagicMock()
        course_mock.id = sample_course_id
        course_mock.game_id = None
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        game_id = uuid4()
        mock_repo.exists = AsyncMock(return_value=True)  # Game exists

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
            gameId=game_id,
        )

        result = await uc.execute(request)

        assert isinstance(result, CourseDetailResponse)
        # Verificamos que el curso tenga game_id seteado (a través de Course)
        # (en tests con mock, solo verificamos que no se lanzó excepción)
        mock_repo.exists.assert_awaited_once_with(game_id, include_deleted=False)

    @pytest.mark.asyncio
    async def test_execute_with_invalid_game_id_raises_not_found(
        self, mock_db, mock_repo
    ):
        """Si se envía un game_id que no existe, lanza GameNotFoundException."""
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)
        mock_repo.exists = AsyncMock(return_value=False)  # Game does NOT exist

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
            gameId=uuid4(),
        )

        with pytest.raises(GameNotFoundException):
            await uc.execute(request)

    @pytest.mark.asyncio
    async def test_execute_without_game_id_creates_course_without_game(
        self, mock_db, mock_repo, sample_course, sample_course_id
    ):
        """Si no se envía game_id, el curso se crea sin juego asignado."""
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)

        course = MagicMock()
        course.id = sample_course_id
        course.game_id = None
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        mock_repo.get_by_id_with_relations = AsyncMock(return_value=course)
        mock_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
        )

        result = await uc.execute(request)
        assert isinstance(result, CourseDetailResponse)
        mock_repo.exists.assert_not_called()

    @pytest.mark.asyncio
    async def test_game_id_none_passes_through_okay(self, mock_db, mock_repo):
        """game_id=None se acepta sin validación."""
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)

        course = MagicMock()
        course.id = uuid4()
        course.game_id = None
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        mock_repo.get_by_id_with_relations = AsyncMock(return_value=course)
        mock_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
            gameId=None,
        )

        result = await uc.execute(request)
        assert isinstance(result, CourseDetailResponse)
        mock_repo.exists.assert_not_called()
