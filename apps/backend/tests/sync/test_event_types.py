"""
Unit tests for EventType enum.

Tests verify:
- classify() returns correct category
- is_simple() works correctly
- is_complex() works correctly
"""

import pytest
from src.sync.domain.event_types import SyncEventType


class TestSyncEventTypeClassify:
    """Test suite for classify() method."""

    @pytest.mark.parametrize(
        "event_type,expected",
        [
            (SyncEventType.LEVEL_TIME, SyncEventType.SIMPLE),
            (SyncEventType.ATTEMPT, SyncEventType.SIMPLE),
            (SyncEventType.SCORE, SyncEventType.SIMPLE),
            (SyncEventType.LEVEL_COMPLETED, SyncEventType.SIMPLE),
            (SyncEventType.DIFFICULTY_CHANGED, SyncEventType.SIMPLE),
            (SyncEventType.ADAPTATION, SyncEventType.SIMPLE),
            (SyncEventType.ERROR, SyncEventType.COMPLEX),
            (SyncEventType.INTERACTION, SyncEventType.COMPLEX),
            (SyncEventType.HINT_USED, SyncEventType.COMPLEX),
        ],
    )
    def test_classify_returns_correct_category(self, event_type, expected):
        """Test that classify() returns the correct category for each event type."""
        result = SyncEventType.classify(event_type)
        assert result == expected

    def test_classify_unknown_event_raises_value_error(self):
        """Test that classify() raises ValueError for unknown event types."""
        with pytest.raises(ValueError, match="Tipo de evento desconocido"):
            SyncEventType.classify("unknown_event")


class TestSyncEventTypeIsSimple:
    """Test suite for is_simple() method."""

    @pytest.mark.parametrize(
        "event_type",
        [
            SyncEventType.LEVEL_TIME,
            SyncEventType.ATTEMPT,
            SyncEventType.SCORE,
            SyncEventType.LEVEL_COMPLETED,
            SyncEventType.DIFFICULTY_CHANGED,
            SyncEventType.ADAPTATION,
        ],
    )
    def test_is_simple_returns_true_for_simple_events(self, event_type):
        """Test that is_simple() returns True for simple event types."""
        assert SyncEventType.is_simple(event_type) is True

    @pytest.mark.parametrize(
        "event_type",
        [
            SyncEventType.ERROR,
            SyncEventType.INTERACTION,
            SyncEventType.HINT_USED,
        ],
    )
    def test_is_simple_returns_false_for_complex_events(self, event_type):
        """Test that is_simple() returns False for complex event types."""
        assert SyncEventType.is_simple(event_type) is False


class TestSyncEventTypeIsComplex:
    """Test suite for is_complex() method."""

    @pytest.mark.parametrize(
        "event_type",
        [
            SyncEventType.ERROR,
            SyncEventType.INTERACTION,
            SyncEventType.HINT_USED,
        ],
    )
    def test_is_complex_returns_true_for_complex_events(self, event_type):
        """Test that is_complex() returns True for complex event types."""
        assert SyncEventType.is_complex(event_type) is True

    @pytest.mark.parametrize(
        "event_type",
        [
            SyncEventType.LEVEL_TIME,
            SyncEventType.ATTEMPT,
            SyncEventType.SCORE,
            SyncEventType.LEVEL_COMPLETED,
            SyncEventType.DIFFICULTY_CHANGED,
            SyncEventType.ADAPTATION,
        ],
    )
    def test_is_complex_returns_false_for_simple_events(self, event_type):
        """Test that is_complex() returns False for simple event types."""
        assert SyncEventType.is_complex(event_type) is False


class TestSyncEventTypeHelpers:
    """Test suite for helper methods."""

    def test_get_all_simple_returns_list(self):
        """Test that get_all_simple() returns a list of simple event types."""
        result = SyncEventType.get_all_simple()
        assert isinstance(result, list)
        assert len(result) == 6
        assert "level_time" in result
        assert "attempt" in result

    def test_get_all_complex_returns_list(self):
        """Test that get_all_complex() returns a list of complex event types."""
        result = SyncEventType.get_all_complex()
        assert isinstance(result, list)
        assert len(result) == 3
        assert "error" in result
        assert "interaction" in result
        assert "hint_used" in result
