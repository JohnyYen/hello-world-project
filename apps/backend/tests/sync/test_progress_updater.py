"""
Unit tests for Progress Updater.

Tests verify:
- increments attempt_count
- updates score
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.handler.progress_updater import ProgressUpdater
from src.sync.domain.sync_event import SyncEvent
from src.statistic.domain.progress import Progress


class TestProgressUpdater:
    """Test suite for ProgressUpdater."""

    @pytest.mark.asyncio
    async def test_updates_attempt_count(self):
        """Test that attempt event increments attempt_count."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.attempt_count = 5
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 10,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1] == {"attempt_count": 10}

    @pytest.mark.asyncio
    async def test_updates_efficiency_rating(self):
        """Test that score event updates efficiency_rating."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.efficiency_rating = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "score"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "rating": 85,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1] == {"efficiency_rating": 85}

    @pytest.mark.asyncio
    async def test_creates_new_progress_when_not_found(self):
        """Test that new progress is created when none exists."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_repository.get_by_student_and_segment = AsyncMock(return_value=None)
        mock_repository.create = AsyncMock()
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 5,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_updates_error_count(self):
        """Test that error event updates error_count."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.error_count = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 3,
            "details": {"error": "test error"},
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["error_count"] == 3
        assert call_args[0][1]["errors_details"] == {"error": "test error"}

    @pytest.mark.asyncio
    async def test_updates_hints_used_count(self):
        """Test that hint_used event updates hints_used_count."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.hints_used_count = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "hint_used"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 2,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["hints_used_count"] == 2

    @pytest.mark.asyncio
    async def test_updates_objectives_completed(self):
        """Test that level_completed event updates objectives_completed."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.objectives_completed = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_completed"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 5,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["objectives_completed"] == 5

    @pytest.mark.asyncio
    async def test_handles_missing_student_id(self):
        """Test that event without student_id is handled gracefully."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {"segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_missing_segment_level_id(self):
        """Test that event without segment_level_id is handled gracefully."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {"student_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_level_time_without_updates(self):
        """Test that level_time event doesn't update any fields."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.payload = {"student_id": 1, "segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_not_called()
