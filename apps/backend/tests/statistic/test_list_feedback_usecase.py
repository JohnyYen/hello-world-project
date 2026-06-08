"""
Unit tests for ListFeedbackUseCase.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from fastapi import HTTPException, status

from src.statistic.application.usecase.list_feedback_usecase import (
    ListFeedbackUseCase,
)
from src.statistic.api.v1.schemas.feedback import (
    FeedbackListResponse,
    FeedbackSchema,
)
from src.users.domain.user import User
from src.users.domain.professor import Professor


def _make_feedback_mock(
    *,
    student_id: UUID | None = None,
    professor_id: UUID | None = None,
    course_id: UUID | None = None,
    comments: str = "ok",
    rating: int = 4,
    feedback_type: str = "advice",
    display_in_game: bool = False,
):
    """Build a mock that matches the FeedbackSchema validation surface."""
    fb = MagicMock()
    fb.id = uuid4()
    fb.student_id = student_id or uuid4()
    fb.professor_id = professor_id or uuid4()
    fb.course_id = course_id
    fb.comments = comments
    fb.rating = rating
    fb.feedback_type = feedback_type
    fb.display_in_game = display_in_game
    fb.acknowledged_at = None
    fb.updated_at = None
    fb.game_id = None
    fb.level_id = None
    fb.created_at = datetime.now()
    return fb


class TestListFeedbackUseCaseInitialization:
    """Test suite for UseCase initialization."""

    def test_init_creates_instance_with_dependencies(self):
        """Test that UseCase can be instantiated with db, feedback_service, and current_user."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        assert use_case is not None
        assert use_case.db == mock_db
        assert use_case.feedback_service == mock_feedback_service
        assert use_case.current_user == mock_current_user


class TestListFeedbackUseCaseExecute:
    """Test suite for execute method."""

    @pytest.mark.asyncio
    async def test_execute_raises_403_when_no_professor_profile(self):
        """Test that execute raises 403 when current_user has no professor profile."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_current_user.professor = None
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(student_id=uuid4())
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "professor profile" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_returns_empty_when_professor_has_no_courses(self):
        """Test that execute returns empty list when professor has no courses."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return no courses
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        result = await use_case.execute(student_id=uuid4())
        
        assert isinstance(result, FeedbackListResponse)
        assert result.items == []
        assert result.total == 0
        assert result.skip == 0
        assert result.limit == 100

    @pytest.mark.asyncio
    async def test_execute_returns_feedback_for_student_in_professors_courses(self):
        """Test that execute returns feedback for student in professor's courses."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return course IDs
        mock_course_result = MagicMock()
        mock_course_result.scalars().all.return_value = [uuid4(), uuid4()]  # Two course IDs
        mock_db.execute = AsyncMock(return_value=mock_course_result)
        
        # Mock feedback_service.get_feedback_for_student to return feedbacks
        mock_feedback1 = MagicMock()
        mock_feedback1.id = uuid4()
        mock_feedback1.student_id = uuid4()
        mock_feedback1.professor_id = mock_professor.id
        mock_feedback1.course_id = None
        mock_feedback1.comments = "Great progress"
        mock_feedback1.rating = 4
        mock_feedback1.feedback_type = "advice"
        mock_feedback1.display_in_game = False
        mock_feedback1.acknowledged_at = None
        mock_feedback1.updated_at = None
        mock_feedback1.game_id = None
        mock_feedback1.level_id = None
        mock_feedback1.created_at = datetime.now()
        
        mock_feedback2 = MagicMock()
        mock_feedback2.id = uuid4()
        mock_feedback2.student_id = uuid4()
        mock_feedback2.professor_id = mock_professor.id
        mock_feedback2.course_id = None
        mock_feedback2.comments = "Good job"
        mock_feedback2.rating = 5
        mock_feedback2.feedback_type = "hint"
        mock_feedback2.display_in_game = True
        mock_feedback2.acknowledged_at = None
        mock_feedback2.updated_at = None
        mock_feedback2.game_id = None
        mock_feedback2.level_id = None
        mock_feedback2.created_at = datetime.now()
        
        mock_feedback_service.get_feedback_for_student = AsyncMock(
            return_value=[mock_feedback1, mock_feedback2]
        )
        
        # Mock feedback_service.count to return total count
        mock_feedback_service.count = AsyncMock(return_value=2)
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        student_id = uuid4()
        result = await use_case.execute(student_id=student_id, skip=0, limit=10)
        
        # Verify feedback_service.get_feedback_for_student was called with correct params
        mock_feedback_service.get_feedback_for_student.assert_called_once_with(
            student_id=student_id,
            course_ids=[mock_course_result.scalars().all.return_value[0], 
                       mock_course_result.scalars().all.return_value[1]],
            skip=0,
            limit=10
        )
        
        # Verify feedback_service.count was called
        mock_feedback_service.count.assert_called_once()
        
        # Verify result
        assert isinstance(result, FeedbackListResponse)
        assert len(result.items) == 2
        assert result.items[0].id == mock_feedback1.id
        assert result.items[0].comments == mock_feedback1.comments
        assert result.items[0].rating == mock_feedback1.rating
        assert result.items[0].feedback_type.value == mock_feedback1.feedback_type
        assert result.items[0].display_in_game == mock_feedback1.display_in_game
        assert result.items[1].id == mock_feedback2.id
        assert result.items[1].comments == mock_feedback2.comments
        assert result.items[1].rating == mock_feedback2.rating
        assert result.items[1].feedback_type.value == mock_feedback2.feedback_type
        assert result.items[1].display_in_game == mock_feedback2.display_in_game
        assert result.total == 2
        assert result.skip == 0
        assert result.limit == 10

    @pytest.mark.asyncio
    async def test_execute_applies_pagination_correctly(self):
        """Test that execute applies skip and limit parameters correctly."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return course IDs
        mock_course_result = MagicMock()
        mock_course_result.scalars().all.return_value = [uuid4()]
        mock_db.execute = AsyncMock(return_value=mock_course_result)
        
        # Mock feedback_service.get_feedback_for_student to return feedbacks
        mock_feedback_service.get_feedback_for_student = AsyncMock(return_value=[])
        
        # Mock feedback_service.count to return total count
        mock_feedback_service.count = AsyncMock(return_value=0)
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        student_id = uuid4()
        await use_case.execute(student_id=student_id, skip=5, limit=10)
        
        # Verify pagination parameters were passed correctly
        mock_feedback_service.get_feedback_for_student.assert_called_once_with(
            student_id=student_id,
            course_ids=[mock_course_result.scalars().all.return_value[0]],
            skip=5,
            limit=10
        )


class TestListFeedbackUseCaseExecuteByCourse:
    """Test suite for execute_by_course method."""

    @pytest.mark.asyncio
    async def test_execute_by_course_raises_403_when_no_professor_profile(self):
        """Test that execute_by_course raises 403 when current_user has no professor profile."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_current_user.professor = None
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute_by_course(course_id=uuid4())
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "professor profile" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_by_course_raises_403_when_professor_does_not_teach_course(self):
        """Test that execute_by_course raises 403 when professor does not teach the course."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return no course_professor link
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute_by_course(course_id=uuid4())
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Professor does not teach this course" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_by_course_returns_feedback_for_course(self):
        """Test that execute_by_course returns feedback for course when professor teaches it."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return course_professor link
        mock_course_prof_result = MagicMock()
        mock_course_prof_result.scalar_one_or_none.return_value = MagicMock()
        mock_db.execute = AsyncMock(return_value=mock_course_prof_result)
        
        # Mock feedback_service.get_feedback_for_course to return feedbacks
        mock_feedback1 = MagicMock()
        mock_feedback1.id = uuid4()
        mock_feedback1.student_id = uuid4()
        mock_feedback1.professor_id = mock_professor.id
        mock_feedback1.course_id = None
        mock_feedback1.comments = "Great progress"
        mock_feedback1.rating = 4
        mock_feedback1.feedback_type = "advice"
        mock_feedback1.display_in_game = False
        mock_feedback1.acknowledged_at = None
        mock_feedback1.updated_at = None
        mock_feedback1.game_id = None
        mock_feedback1.level_id = None
        mock_feedback1.created_at = datetime.now()
        
        mock_feedback_service.get_feedback_for_course = AsyncMock(
            return_value=[mock_feedback1]
        )
        
        # Mock feedback_service.count to return total count
        mock_feedback_service.count = AsyncMock(return_value=1)
        
        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        course_id = uuid4()
        result = await use_case.execute_by_course(course_id=course_id, skip=0, limit=10)

        # Verify feedback_service.get_feedback_for_course was called with correct params
        mock_feedback_service.get_feedback_for_course.assert_called_once_with(
            course_id=course_id,
            skip=0,
            limit=10
        )

        # Verify feedback_service.count was called
        mock_feedback_service.count.assert_called_once()

        # Verify result
        assert isinstance(result, FeedbackListResponse)
        assert len(result.items) == 1
        assert result.items[0].id == mock_feedback1.id
        assert result.items[0].comments == mock_feedback1.comments
        assert result.items[0].rating == mock_feedback1.rating
        assert result.items[0].feedback_type.value == mock_feedback1.feedback_type
        assert result.items[0].display_in_game == mock_feedback1.display_in_game
        assert result.total == 1
        assert result.skip == 0
        assert result.limit == 10


class TestListFeedbackUseCaseStudentIdResolver:
    """
    Regression tests for the User.id vs students.id mismatch and the
    NULL course_id IN-clause problem.

    The /dashboard/students/{user_id} URL sends the User.id, but
    feedbacks.student_id FK points to students.id. Additionally, the
    submit form allows course_id=NULL, and the previous
    `course_id IN (professor's_courses)` filter excluded those rows
    because SQL's `NULL IN (...)` is always UNKNOWN.
    """

    @pytest.mark.asyncio
    async def test_execute_resolves_user_id_to_students_id(self):
        """URL sends User.id; the use case must resolve to students.id before querying."""
        submitted_user_id = uuid4()
        canonical_students_id = uuid4()
        professor_course_id = uuid4()

        mock_db = MagicMock()
        # 1st execute: CourseProfessor.course_id for the professor
        course_result = MagicMock()
        course_result.scalars().all.return_value = [professor_course_id]
        # 2nd execute: Student.id == submitted_user_id  -> not found (it is a User.id)
        direct_result = MagicMock()
        direct_result.scalar_one_or_none.return_value = None
        # 3rd execute: Student.user_id == submitted_user_id -> returns Student
        student_mock = MagicMock()
        student_mock.id = canonical_students_id
        by_user_result = MagicMock()
        by_user_result.scalar_one_or_none.return_value = student_mock
        mock_db.execute = AsyncMock(
            side_effect=[course_result, direct_result, by_user_result]
        )

        mock_feedback_service = MagicMock()
        mock_feedback_service.get_feedback_for_student_with_null_courses = AsyncMock(
            return_value=[]
        )
        mock_feedback_service.count_feedback_for_student_with_null_courses = AsyncMock(
            return_value=0
        )

        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor

        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user,
        )

        await use_case.execute(student_id=submitted_user_id)

        # The service MUST receive the canonical students.id, not the User.id
        list_call = (
            mock_feedback_service.get_feedback_for_student_with_null_courses.call_args
        )
        assert list_call.kwargs["student_id"] == canonical_students_id
        assert list_call.kwargs["student_id"] != submitted_user_id

        count_call = (
            mock_feedback_service.count_feedback_for_student_with_null_courses.call_args
        )
        assert count_call.kwargs["student_id"] == canonical_students_id

    @pytest.mark.asyncio
    async def test_execute_returns_feedback_with_null_course_id(self):
        """Feedback where course_id=NULL must be visible in the history view."""
        professor_course_id = uuid4()
        canonical_students_id = uuid4()

        mock_db = MagicMock()
        course_result = MagicMock()
        course_result.scalars().all.return_value = [professor_course_id]
        # Resolver fast path: submitted id IS already a students.id
        direct_result = MagicMock()
        direct_result.scalar_one_or_none.return_value = MagicMock()
        mock_db.execute = AsyncMock(side_effect=[course_result, direct_result])

        null_course_feedback = _make_feedback_mock(
            student_id=canonical_students_id,
            course_id=None,
            comments="Buen trabajo",
        )
        mock_feedback_service = MagicMock()
        mock_feedback_service.get_feedback_for_student_with_null_courses = AsyncMock(
            return_value=[null_course_feedback]
        )
        mock_feedback_service.count_feedback_for_student_with_null_courses = AsyncMock(
            return_value=1
        )

        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor

        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user,
        )

        result = await use_case.execute(student_id=canonical_students_id)

        # The new service method is used (so NULL/IN semantics apply)
        mock_feedback_service.get_feedback_for_student_with_null_courses.assert_called_once()
        mock_feedback_service.count_feedback_for_student_with_null_courses.assert_called_once()

        # The NULL-course feedback shows up in the response
        assert isinstance(result, FeedbackListResponse)
        assert len(result.items) == 1
        assert result.items[0].course_id is None
        assert result.items[0].comments == "Buen trabajo"
        assert result.total == 1

    @pytest.mark.asyncio
    async def test_execute_passes_professor_courses_for_non_null_filtering(self):
        """
        When course_id is NOT null, the use case must still narrow the result
        set to the professor's own courses. The new service method receives
        the course_ids list and is responsible for the IN clause.
        """
        professor_course_id = uuid4()
        other_professors_course_id = uuid4()
        canonical_students_id = uuid4()

        mock_db = MagicMock()
        course_result = MagicMock()
        course_result.scalars().all.return_value = [professor_course_id]
        direct_result = MagicMock()
        direct_result.scalar_one_or_none.return_value = MagicMock()
        mock_db.execute = AsyncMock(side_effect=[course_result, direct_result])

        mock_feedback_service = MagicMock()
        mock_feedback_service.get_feedback_for_student_with_null_courses = AsyncMock(
            return_value=[]
        )
        mock_feedback_service.count_feedback_for_student_with_null_courses = AsyncMock(
            return_value=0
        )

        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor

        use_case = ListFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user,
        )

        await use_case.execute(student_id=canonical_students_id)

        list_call = (
            mock_feedback_service.get_feedback_for_student_with_null_courses.call_args
        )
        # The professor's own courses are forwarded, and ONLY those
        assert list_call.kwargs["course_ids"] == [professor_course_id]
        assert other_professors_course_id not in list_call.kwargs["course_ids"]

        count_call = (
            mock_feedback_service.count_feedback_for_student_with_null_courses.call_args
        )
        assert count_call.kwargs["course_ids"] == [professor_course_id]