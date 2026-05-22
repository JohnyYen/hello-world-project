import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
from src.course.domain.course_professor import CourseProfessor
from src.course.infrastructure.course_repository import CourseRepository


class TestCourseRepositoryGetByIdWithRelations:
    @pytest.mark.asyncio
    async def test_get_by_id_with_relations_returns_course_with_enrollments_and_professors(
        self, mock_db, sample_course, sample_course_id
    ):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=sample_course)
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.get_by_id_with_relations(sample_course_id)

        assert result is not None
        assert result.id == sample_course_id
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_relations_returns_none_when_not_found(self, mock_db):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.get_by_id_with_relations(uuid4())

        assert result is None


class TestCourseRepositoryBulkCreateEnrollments:
    @pytest.mark.asyncio
    async def test_bulk_create_enrollments_inserts_n_records(self, mock_db):
        course_id = uuid4()
        student_ids = [uuid4(), uuid4(), uuid4()]

        repo = CourseRepository(mock_db)
        result = await repo.bulk_create_enrollments(course_id, student_ids)

        assert len(result) == 3
        assert all(isinstance(e, CourseEnrollment) for e in result)
        assert all(e.course_id == course_id for e in result)
        mock_db.add_all.assert_called_once()
        mock_db.flush.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_bulk_create_enrollments_empty_list(self, mock_db):
        repo = CourseRepository(mock_db)
        result = await repo.bulk_create_enrollments(uuid4(), [])

        assert len(result) == 0
        mock_db.add_all.assert_called_once_with([])

    @pytest.mark.asyncio
    async def test_bulk_create_professors_inserts_n_records(self, mock_db):
        course_id = uuid4()
        professor_ids = [uuid4(), uuid4()]

        repo = CourseRepository(mock_db)
        result = await repo.bulk_create_professors(course_id, professor_ids)

        assert len(result) == 2
        assert all(isinstance(p, CourseProfessor) for p in result)
        assert all(p.course_id == course_id for p in result)
        mock_db.add_all.assert_called_once()
        mock_db.flush.assert_awaited_once()


class TestCourseRepositorySoftDelete:
    @pytest.mark.asyncio
    async def test_soft_delete_enrollments_for_course_updates_deleted_at(self, mock_db):
        mock_result = MagicMock()
        mock_result.rowcount = 3
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.soft_delete_enrollments_for_course(uuid4())

        assert result == 3
        mock_db.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_soft_delete_enrollments_returns_zero_when_none_active(self, mock_db):
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.soft_delete_enrollments_for_course(uuid4())

        assert result == 0

    @pytest.mark.asyncio
    async def test_soft_delete_professors_for_course_updates_deleted_at(self, mock_db):
        mock_result = MagicMock()
        mock_result.rowcount = 2
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.soft_delete_professors_for_course(uuid4())

        assert result == 2

    @pytest.mark.asyncio
    async def test_soft_delete_course_returns_true_when_deleted(self, mock_db):
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.soft_delete_course(uuid4())

        assert result is True

    @pytest.mark.asyncio
    async def test_soft_delete_course_returns_false_when_not_found(self, mock_db):
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = CourseRepository(mock_db)
        result = await repo.soft_delete_course(uuid4())

        assert result is False


class TestCourseRepositorySyncStudents:
    @pytest.mark.asyncio
    async def test_sync_students_adds_new_and_removes_old(self, mock_db):
        existing_ids = {uuid4(), uuid4()}
        course_id = uuid4()
        new_student_ids = list(existing_ids) + [uuid4()]

        repo = CourseRepository(mock_db)
        repo.get_existing_enrollment_ids = AsyncMock(return_value=existing_ids)

        await repo.sync_students(course_id, new_student_ids)

        repo.bulk_create_enrollments.assert_awaited_once()
        assert mock_db.execute.await_count >= 1

    @pytest.mark.asyncio
    async def test_sync_students_no_changes(self, mock_db):
        existing_ids = {uuid4(), uuid4()}
        course_id = uuid4()
        same_ids = list(existing_ids)

        repo = CourseRepository(mock_db)
        repo.get_existing_enrollment_ids = AsyncMock(return_value=existing_ids)

        await repo.sync_students(course_id, same_ids)

        repo.bulk_create_enrollments.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_sync_students_removes_all_when_empty_target(self, mock_db):
        existing_ids = {uuid4(), uuid4(), uuid4()}
        course_id = uuid4()

        repo = CourseRepository(mock_db)
        repo.get_existing_enrollment_ids = AsyncMock(return_value=existing_ids)

        await repo.sync_students(course_id, [])

        repo.bulk_create_enrollments.assert_not_awaited()
        assert mock_db.execute.await_count >= 1
