"""
Unit tests for FeedbackCreate schema validation.
"""
import pytest
from pydantic import ValidationError
from uuid import UUID, uuid4
from src.shared.domain.enums import FeedbackType
from src.statistic.api.v1.schemas.feedback import FeedbackCreate


class TestFeedbackCreateSchema:
    """Test suite for FeedbackCreate schema validation."""

    def test_accepts_valid_uuid_student_id(self):
        """Test that FeedbackCreate accepts valid UUID for student_id."""
        valid_uuid = uuid4()
        feedback_data = {
            "student_id": valid_uuid,
            "comments": "Great progress",
            "rating": 4
        }
        feedback = FeedbackCreate(**feedback_data)
        assert feedback.student_id == valid_uuid

    def test_rejects_integer_student_id(self):
        """Test that FeedbackCreate rejects integer for student_id."""
        feedback_data = {
            "student_id": 123,
            "comments": "Great progress",
            "rating": 4
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "student_id" in str(exc_info.value)
        assert "UUID" in str(exc_info.value)

    def test_rejects_invalid_uuid_string(self):
        """Test that FeedbackCreate rejects invalid UUID string."""
        feedback_data = {
            "student_id": "not-a-uuid",
            "comments": "Great progress",
            "rating": 4
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "student_id" in str(exc_info.value)
        assert "UUID" in str(exc_info.value)

    def test_feedback_type_defaults_to_advice(self):
        """Test that FeedbackCreate.feedback_type defaults to advice when omitted."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "Great progress",
            "rating": 4
        }
        feedback = FeedbackCreate(**feedback_data)
        assert feedback.feedback_type == FeedbackType.ADVICE

    def test_accepts_explicit_feedback_type(self):
        """Test that FeedbackCreate accepts explicit feedback_type values."""
        for feedback_type in ["advice", "hint", "tip", "message"]:
            feedback_data = {
                "student_id": uuid4(),
                "comments": "Great progress",
                "rating": 4,
                "feedback_type": feedback_type
            }
            feedback = FeedbackCreate(**feedback_data)
            assert feedback.feedback_type.value == feedback_type

    def test_rejects_rating_below_minimum(self):
        """Test that FeedbackCreate rejects rating < 1."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "Great progress",
            "rating": 0
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "rating" in str(exc_info.value)
        assert "greater than or equal to 1" in str(exc_info.value)

    def test_rejects_rating_above_maximum(self):
        """Test that FeedbackCreate rejects rating > 5."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "Great progress",
            "rating": 6
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "rating" in str(exc_info.value)
        assert "less than or equal to 5" in str(exc_info.value)

    def test_accepts_valid_rating_range(self):
        """Test that FeedbackCreate accepts rating values 1-5."""
        for rating in [1, 2, 3, 4, 5]:
            feedback_data = {
                "student_id": uuid4(),
                "comments": "Great progress",
                "rating": rating
            }
            feedback = FeedbackCreate(**feedback_data)
            assert feedback.rating == rating

    def test_rejects_empty_comments(self):
        """Test that FeedbackCreate rejects empty comments string."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "",
            "rating": 4
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "comments" in str(exc_info.value)
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_accepts_non_empty_comments(self):
        """Test that FeedbackCreate accepts non-empty comments."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "Good job!",
            "rating": 4
        }
        feedback = FeedbackCreate(**feedback_data)
        assert feedback.comments == "Good job!"

    def test_rejects_invalid_feedback_type(self):
        """Test that FeedbackCreate rejects invalid feedback_type values."""
        feedback_data = {
            "student_id": uuid4(),
            "comments": "Great progress",
            "rating": 4,
            "feedback_type": "invalid_type"
        }
        with pytest.raises(ValidationError) as exc_info:
            FeedbackCreate(**feedback_data)
        assert "feedback_type" in str(exc_info.value)
        assert "Input should be" in str(exc_info.value)

    def test_feedback_create_schema_serialization(self):
        """Test FeedbackCreate schema serialization with all fields."""
        student_id = uuid4()
        course_id = uuid4()
        feedback_data = {
            "student_id": student_id,
            "comments": "Excellent work!",
            "rating": 5,
            "feedback_type": "hint",
            "course_id": course_id,
            "display_in_game": True
        }
        feedback = FeedbackCreate(**feedback_data)
        assert feedback.student_id == student_id
        assert feedback.comments == "Excellent work!"
        assert feedback.rating == 5
        assert feedback.feedback_type.value == "hint"
        assert feedback.course_id == course_id
        assert feedback.display_in_game is True