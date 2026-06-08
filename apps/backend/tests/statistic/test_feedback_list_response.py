"""
Unit tests for FeedbackListResponse schema.
"""
from pydantic import ValidationError
from uuid import UUID, uuid4
from src.statistic.api.v1.schemas.feedback import FeedbackListResponse, FeedbackSchema
from datetime import datetime


class TestFeedbackListResponseSchema:
    """Test suite for FeedbackListResponse schema."""

    def test_feedback_list_response_serialization_with_mock_data(self):
        """Test FeedbackListResponse schema serialization with mock data."""
        # Create mock feedback data
        feedback_id = uuid4()
        student_id = uuid4()
        professor_id = uuid4()
        
        feedback_data = {
            "id": feedback_id,
            "student_id": student_id,
            "professor_id": professor_id,
            "comments": "Great progress",
            "rating": 4,
            "feedback_type": "advice",
            "display_in_game": False,
            "created_at": datetime.now()
        }
        
        feedback = FeedbackSchema(**feedback_data)
        
        # Create list response
        list_response_data = {
            "items": [feedback],
            "total": 1,
            "skip": 0,
            "limit": 10
        }
        
        list_response = FeedbackListResponse(**list_response_data)
        
        assert len(list_response.items) == 1
        assert list_response.items[0].id == feedback_id
        assert list_response.items[0].student_id == student_id
        assert list_response.items[0].professor_id == professor_id
        assert list_response.total == 1
        assert list_response.skip == 0
        assert list_response.limit == 10

    def test_feedback_list_response_empty_items(self):
        """Test FeedbackListResponse with empty items list."""
        list_response_data = {
            "items": [],
            "total": 0,
            "skip": 0,
            "limit": 10
        }
        
        list_response = FeedbackListResponse(**list_response_data)
        
        assert len(list_response.items) == 0
        assert list_response.total == 0
        assert list_response.skip == 0
        assert list_response.limit == 10

    def test_feedback_list_response_pagination(self):
        """Test FeedbackListResponse with pagination values."""
        list_response_data = {
            "items": [],
            "total": 25,
            "skip": 10,
            "limit": 5
        }
        
        list_response = FeedbackListResponse(**list_response_data)
        
        assert list_response.total == 25
        assert list_response.skip == 10
        assert list_response.limit == 5