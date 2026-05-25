import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.course.application.usecase.create_course_usecase import CreateCourseUseCase
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest,
    CourseDetailResponse,
    CourseResponse,
    StudentEnrollmentResponse,
    ProfessorAssignmentResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


class TestCreateCourseUseCase:
    @pytest.mark.asyncio
    async def test_execute_happy_path_creates_course_with_enrollments_and_professors(
        self, mock_db, mock_repo, sample_course, sample_course_id
    ):
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)
        mock_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)
        mock_repo.get_students_for_course = AsyncMock(
            return_value=[
                {
                    "student_id": uuid4(),
                    "name": "Juan",
                    "email": "juan@test.com",
                    "enrolled_at": "2025-03-01T00:00:00",
                }
            ]
        )
        mock_repo.get_professors_for_course = AsyncMock(
            return_value=[
                {
                    "professor_id": uuid4(),
                    "name": "María",
                    "email": "maria@test.com",
                }
            ]
        )

        course = MagicMock()
        course.id = sample_course_id
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            description="Curso básico",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
            studentIds=[uuid4()],
            professorIds=[uuid4()],
        )

        result = await uc.execute(request)

        assert result is not None
        assert isinstance(result, CourseDetailResponse)
        mock_repo.get_one_by_filters.assert_awaited_once()
        mock_repo.bulk_create_enrollments.assert_awaited_once()
        mock_repo.bulk_create_professors.assert_awaited_once()
        mock_db.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_execute_duplicate_school_year_and_period_raises_exception(
        self, mock_db, mock_repo
    ):
        mock_repo.get_one_by_filters = AsyncMock(
            return_value=MagicMock()
        )

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
        )

        with pytest.raises(DuplicateEntryException):
            await uc.execute(request)

        mock_repo.bulk_create_enrollments.assert_not_called()
        mock_repo.bulk_create_professors.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_empty_student_ids_creates_course_with_zero_enrollments(
        self, mock_db, mock_repo, sample_course, sample_course_id
    ):
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)

        course = MagicMock()
        course.id = sample_course_id
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()

        mock_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)
        mock_repo.get_students_for_course = AsyncMock(return_value=[])
        mock_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Matemáticas",
            description="Curso sin estudiantes",
            schoolYear="2025-2026",
            periodLabel="Semestre 1",
            startDate=date(2025, 3, 1),
            endDate=date(2025, 7, 15),
        )

        result = await uc.execute(request)

        assert result is not None
        assert len(result.students) == 0
        mock_repo.bulk_create_enrollments.assert_not_called()
        mock_repo.bulk_create_professors.assert_not_called()

    @pytest.mark.asyncio
    async def test_build_detail_response_raises_not_found(
        self, mock_db, mock_repo
    ):
        mock_repo.get_by_id_with_relations = AsyncMock(return_value=None)

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        with pytest.raises(NotFoundException):
            await uc._build_detail_response(uuid4())

    @pytest.mark.asyncio
    async def test_execute_with_only_students_no_professors(
        self, mock_db, mock_repo, sample_course, sample_course_id
    ):
        mock_repo.get_one_by_filters = AsyncMock(return_value=None)

        course = MagicMock()
        course.id = sample_course_id
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()

        mock_repo.get_by_id_with_relations = AsyncMock(return_value=sample_course)
        mock_repo.get_students_for_course = AsyncMock(
            return_value=[
                {
                    "student_id": uuid4(),
                    "name": "Ana",
                    "email": "ana@test.com",
                    "enrolled_at": "2025-03-01T00:00:00",
                }
            ]
        )
        mock_repo.get_professors_for_course = AsyncMock(return_value=[])

        uc = CreateCourseUseCase(db=mock_db, course_repo=mock_repo)

        request = CourseCreateRequest(
            name="Física",
            schoolYear="2025-2026",
            periodLabel="Semestre 2",
            startDate=date(2025, 8, 1),
            endDate=date(2025, 12, 15),
            studentIds=[uuid4()],
        )

        result = await uc.execute(request)

        assert result is not None
        mock_repo.bulk_create_enrollments.assert_awaited_once()
        mock_repo.bulk_create_professors.assert_not_called()
