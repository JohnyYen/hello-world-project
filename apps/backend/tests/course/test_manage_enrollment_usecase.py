import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from uuid import uuid4

from src.course.application.usecase.manage_enrollment_usecase import (
    ManageEnrollmentUseCase,
)
from src.shared.domain.exceptions import NotFoundException


class TestManageEnrollmentUseCase:
    @pytest.mark.asyncio
    async def test_enroll_students_deduplicates_already_enrolled(
        self, mock_db, mock_repo
    ):
        course_id = uuid4()
        existing_id = uuid4()
        new_id = uuid4()

        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.get_existing_enrollment_ids = AsyncMock(
            return_value={existing_id}
        )
        mock_repo.get_students_for_course = AsyncMock(
            return_value=[
                {
                    "student_id": new_id,
                    "name": "New Student",
                    "email": "new@test.com",
                    "enrolled_at": "2025-03-01T00:00:00",
                }
            ]
        )

        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.enroll_students(course_id, [existing_id, new_id])

        assert len(result) == 1
        mock_repo.bulk_create_enrollments.assert_awaited_once_with(course_id, [new_id])

    @pytest.mark.asyncio
    async def test_enroll_students_all_already_enrolled_skips_create(
        self, mock_db, mock_repo
    ):
        course_id = uuid4()
        existing_id = uuid4()

        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.get_existing_enrollment_ids = AsyncMock(
            return_value={existing_id}
        )
        mock_repo.get_students_for_course = AsyncMock(return_value=[])

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.enroll_students(course_id, [existing_id])

        mock_repo.bulk_create_enrollments.assert_not_called()

    @pytest.mark.asyncio
    async def test_enroll_students_on_non_existent_course_raises_404(
        self, mock_db, mock_repo
    ):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)

        with pytest.raises(NotFoundException):
            await uc.enroll_students(uuid4(), [uuid4()])

    @pytest.mark.asyncio
    async def test_unenroll_student_soft_deletes_enrollment(
        self, mock_db, mock_repo
    ):
        course_id = uuid4()
        student_id = uuid4()

        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.get_existing_enrollment_ids = AsyncMock(
            return_value={student_id}
        )

        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.unenroll_student(course_id, student_id)

        assert result is True

    @pytest.mark.asyncio
    async def test_unenroll_student_not_enrolled_returns_false(
        self, mock_db, mock_repo
    ):
        course_id = uuid4()
        student_id = uuid4()

        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.get_existing_enrollment_ids = AsyncMock(return_value=set())

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.unenroll_student(course_id, student_id)

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_course_cascade_soft_deletes_all(
        self, mock_db, mock_repo
    ):
        course_id = uuid4()

        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.soft_delete_enrollments_for_course = AsyncMock(return_value=3)
        mock_repo.soft_delete_professors_for_course = AsyncMock(return_value=2)
        mock_repo.soft_delete_course = AsyncMock(return_value=True)

        mock_db.begin = MagicMock()
        mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.delete_course(course_id)

        assert result is True
        mock_repo.soft_delete_enrollments_for_course.assert_awaited_once_with(course_id)
        mock_repo.soft_delete_professors_for_course.assert_awaited_once_with(course_id)
        mock_repo.soft_delete_course.assert_awaited_once_with(course_id)

    @pytest.mark.asyncio
    async def test_delete_course_on_non_existent_raises_404(
        self, mock_db, mock_repo
    ):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)

        with pytest.raises(NotFoundException):
            await uc.delete_course(uuid4())

    @pytest.mark.asyncio
    async def test_get_students_returns_list(self, mock_db, mock_repo):
        course_id = uuid4()
        mock_repo.get_by_id = AsyncMock(return_value=MagicMock())
        mock_repo.get_students_for_course = AsyncMock(
            return_value=[
                {
                    "student_id": uuid4(),
                    "name": "Student",
                    "email": "s@test.com",
                    "enrolled_at": "2025-03-01T00:00:00",
                }
            ]
        )

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)
        result = await uc.get_students(course_id)

        assert len(result) == 1
        assert result[0].name == "Student"

    @pytest.mark.asyncio
    async def test_get_students_on_non_existent_course_raises_404(
        self, mock_db, mock_repo
    ):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        uc = ManageEnrollmentUseCase(db=mock_db, course_repo=mock_repo)

        with pytest.raises(NotFoundException):
            await uc.get_students(uuid4())
