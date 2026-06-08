"""
Unit tests for FeedbackType enum.
"""
from src.shared.domain.enums import FeedbackType


class TestFeedbackTypeEnum:
    """Test suite for FeedbackType enum."""

    def test_feedback_type_has_exactly_four_values(self):
        """Test that FeedbackType has exactly 4 values: advice, hint, tip, message."""
        expected_values = {"advice", "hint", "tip", "message"}
        actual_values = {e.value for e in FeedbackType}
        assert actual_values == expected_values

    def test_feedback_type_advice_value(self):
        """Test that FeedbackType.ADVICE has value 'advice'."""
        assert FeedbackType.ADVICE.value == "advice"

    def test_feedback_type_hint_value(self):
        """Test that FeedbackType.HINT has value 'hint'."""
        assert FeedbackType.HINT.value == "hint"

    def test_feedback_type_tip_value(self):
        """Test that FeedbackType.TIP has value 'tip'."""
        assert FeedbackType.TIP.value == "tip"

    def test_feedback_type_message_value(self):
        """Test that FeedbackType.MESSAGE has value 'message'."""
        assert FeedbackType.MESSAGE.value == "message"