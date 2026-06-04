"""
Unit tests for CreateFeedbackUseCase.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from fastapi import HTTPException, status

from src.statistic.application.usecase.create_feedback_usecase import (
    CreateFeedbackUseCase,
)
from src.statistic.api.v1.schemas.feedback import FeedbackCreate
from src.users.domain.user import User
from src.users.domain.professor import Professor


class TestCreateFeedbackUseCaseInitialization:
    """Test suite for UseCase initialization."""

    def test_init_creates_instance_with_dependencies(self):
        """Test that UseCase can be instantiated with db, feedback_service, and current_user."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        assert use_case is not None
        assert use_case.db == mock_db
        assert use_case.feedback_service == mock_feedback_service
        assert use_case.current_user == mock_current_user


class TestCreateFeedbackUseCaseExecute:
    """Test suite for execute method."""

    @pytest.mark.asyncio
    async def test_execute_raises_403_when_no_professor_profile(self):
        """Test that execute raises 403 when current_user has no professor profile."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_current_user.professor = None
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "professor profile" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_raises_404_when_course_not_found(self):
        """Test that execute raises 404 when course_id doesn't exist."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return None for course query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4,
            course_id=uuid4()  # Non-existent course
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Course not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_raises_403_when_student_not_enrolled_in_course(self):
        """Test that execute raises 403 when student is not enrolled in the course."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return course but not enrollment
        mock_course_result = MagicMock()
        mock_course_result.scalar_one_or_none.return_value = MagicMock()  # Course exists
        
        mock_enrollment_result = MagicMock()
        mock_enrollment_result.scalar_one_or_none.return_value = None  # No enrollment
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result])
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4,
            course_id=uuid4()
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Student is not enrolled in this course" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_raises_403_when_professor_does_not_teach_course(self):
        """Test that execute raises 403 when professor does not teach the course."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return course, enrollment, but no course_professor link
        mock_course_result = MagicMock()
        mock_course_result.scalar_one_or_none.return_value = MagicMock()  # Course exists
        
        mock_enrollment_result = MagicMock()
        mock_enrollment_result.scalar_one_or_none.return_value = MagicMock()  # Enrollment exists
        
        mock_course_prof_result = MagicMock()
        mock_course_prof_result.scalar_one_or_none.return_value = None  # No professor-course link
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result, mock_course_prof_result])
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4,
            course_id=uuid4()
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Professor does not teach this course" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_creates_feedback_successfully(self):
        """Test that execute creates feedback successfully when all validations pass."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return valid course, enrollment, and course_professor
        mock_course_result = MagicMock()
        mock_course_result.scalar_one_or_none.return_value = MagicMock()  # Course exists
        
        mock_enrollment_result = MagicMock()
        mock_enrollment_result.scalar_one_or_none.return_value = MagicMock()  # Enrollment exists
        
        mock_course_prof_result = MagicMock()
        mock_course_prof_result.scalar_one_or_none.return_value = MagicMock()  # Professor-course link exists
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result, mock_course_prof_result])
        
        # Mock feedback_service.create to return a feedback object
        course_id = uuid4()
        student_id = uuid4()
        mock_feedback = MagicMock()
        mock_feedback.id = uuid4()
        mock_feedback.student_id = student_id
        mock_feedback.professor_id = mock_professor.id
        mock_feedback.course_id = course_id
        mock_feedback.comments = "Great progress"
        mock_feedback.rating = 4
        mock_feedback.feedback_type = "advice"
        mock_feedback.display_in_game = False
        mock_feedback.acknowledged_at = None
        mock_feedback.updated_at = None
        mock_feedback.game_id = None
        mock_feedback.level_id = None
        mock_feedback.created_at = datetime.now()
        
        mock_feedback_service.create = AsyncMock(return_value=mock_feedback)
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=student_id,
            comments="Great progress",
            rating=4,
            course_id=course_id
        )
        
        result = await use_case.execute(feedback_data)
        
        # Verify the feedback_service.create was called with correct data
        mock_feedback_service.create.assert_called_once()
        call_args = mock_feedback_service.create.call_args[0][0]
        assert call_args["student_id"] == student_id
        assert call_args["professor_id"] == mock_professor.id
        assert call_args["comments"] == "Great progress"
        assert call_args["rating"] == 4
        assert call_args["course_id"] == course_id
        assert call_args["feedback_type"] == "advice"
        assert call_args["display_in_game"] is False
        
        # Verify the result
        assert result.id == mock_feedback.id
        assert result.student_id == mock_feedback.student_id
        assert result.professor_id == mock_feedback.professor_id
        assert result.comments == mock_feedback.comments
        assert result.rating == mock_feedback.rating
        assert result.feedback_type.value == mock_feedback.feedback_type
        assert result.display_in_game == mock_feedback.display_in_game
        assert result.created_at == mock_feedback.created_at

    @pytest.mark.asyncio
    async def test_execute_resolves_professor_id_correctly(self):
        """Test that _resolve_professor correctly resolves professor_id from current_user."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Mock db.execute to return valid course, enrollment, and course_professor
        mock_course_result = MagicMock()
        mock_course_result.scalar_one_or_none.return_value = MagicMock()
        
        mock_enrollment_result = MagicMock()
        mock_enrollment_result.scalar_one_or_none.return_value = MagicMock()
        
        mock_course_prof_result = MagicMock()
        mock_course_prof_result.scalar_one_or_none.return_value = MagicMock()
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result, mock_course_prof_result])
        
        # Mock feedback_service.create to return a feedback object
        mock_feedback = MagicMock()
        mock_feedback.id = uuid4()
        mock_feedback.student_id = uuid4()
        mock_feedback.professor_id = mock_professor.id
        mock_feedback.course_id = None
        mock_feedback.comments = "Great progress"
        mock_feedback.rating = 4
        mock_feedback.feedback_type = "advice"
        mock_feedback.display_in_game = False
        mock_feedback.acknowledged_at = None
        mock_feedback.updated_at = None
        mock_feedback.game_id = None
        mock_feedback.level_id = None
        mock_feedback.created_at = datetime.now()
        
        mock_feedback_service.create = AsyncMock(return_value=mock_feedback)
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4
        )
        
        result = await use_case.execute(feedback_data)
        
        # Verify professor_id was correctly resolved from current_user.professor.id
        call_args = mock_feedback_service.create.call_args[0][0]
        assert call_args["professor_id"] == mock_professor.id
        assert result.professor_id == mock_professor.id

    @pytest.mark.asyncio
    async def test_execute_raises_403_when_no_professor_profile(self):
        """Test that execute raises 403 when current_user has no professor profile."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_current_user.professor = None
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "professor profile" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_execute_authorizes_course_correctly(self):
        """Test that _authorize_course correctly validates student enrollment and professor teaching."""
        mock_db = MagicMock()
        mock_feedback_service = MagicMock()
        mock_current_user = MagicMock()
        mock_professor = MagicMock()
        mock_professor.id = uuid4()
        mock_current_user.professor = mock_professor
        
        # Test case 1: Student enrolled and professor teaches course -> should succeed
        mock_course_result = MagicMock()
        mock_course_result.scalar_one_or_none.return_value = MagicMock()  # Course exists
        
        mock_enrollment_result = MagicMock()
        mock_enrollment_result.scalar_one_or_none.return_value = MagicMock()  # Enrollment exists
        
        mock_course_prof_result = MagicMock()
        mock_course_prof_result.scalar_one_or_none.return_value = MagicMock()  # Professor teaches course
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result, mock_course_prof_result])
        
        # Mock feedback_service.create to return a feedback object
        mock_feedback = MagicMock()
        mock_feedback.id = uuid4()
        mock_feedback.student_id = uuid4()
        mock_feedback.professor_id = mock_professor.id
        mock_feedback.course_id = uuid4()
        mock_feedback.comments = "Great progress"
        mock_feedback.rating = 4
        mock_feedback.feedback_type = "advice"
        mock_feedback.display_in_game = False
        mock_feedback.acknowledged_at = None
        mock_feedback.updated_at = None
        mock_feedback.game_id = None
        mock_feedback.level_id = None
        mock_feedback.created_at = datetime.now()
        
        mock_feedback_service.create = AsyncMock(return_value=mock_feedback)
        
        use_case = CreateFeedbackUseCase(
            db=mock_db,
            feedback_service=mock_feedback_service,
            current_user=mock_current_user
        )
        
        course_id_param = uuid4()
        feedback_data = FeedbackCreate(
            student_id=uuid4(),
            comments="Great progress",
            rating=4,
            course_id=course_id_param
        )
        
        # Should not raise exception
        result = await use_case.execute(feedback_data)
        assert result is not None
        
        # Test case 2: Student NOT enrolled in course -> should raise 403
        mock_enrollment_result_none = MagicMock()
        mock_enrollment_result_none.scalar_one_or_none.return_value = None  # No enrollment
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result_none])
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Student is not enrolled in this course" in exc_info.value.detail
        
        # Test case 3: Professor does NOT teach course -> should raise 403
        mock_course_prof_result_none = MagicMock()
        mock_course_prof_result_none.scalar_one_or_none.return_value = None  # No professor-course link
        
        mock_db.execute = AsyncMock(side_effect=[mock_course_result, mock_enrollment_result, mock_course_prof_result_none])
        
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(feedback_data)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Professor does not teach this course" in exc_info.value.detail