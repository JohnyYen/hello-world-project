"""
Unit tests for Simple Event Handler.

Tests verify:
- handles level_time event
- handles attempt event
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.handler.simple_event_handler import SimpleEventHandler
from src.sync.domain.sync_event import SyncEvent


class TestSimpleEventHandler:
    """Test suite for SimpleEventHandler."""

    @pytest.mark.asyncio
    async def test_handles_level_time_event(self):
        """Test that handler processes level_time events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.payload = {"student_id": 1, "segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_attempt_event(self):
        """Test that handler processes attempt events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {"student_id": 1, "segment_level_id": 1, "count": 5}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_score_event(self):
        """Test that handler processes score events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "score"
        event.payload = {"student_id": 1, "segment_level_id": 1, "rating": 85}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_level_completed_event(self):
        """Test that handler processes level_completed events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_completed"
        event.payload = {"student_id": 1, "segment_level_id": 1, "count": 10}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_difficulty_changed_event(self):
        """Test that handler processes difficulty_changed events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "difficulty_changed"
        event.payload = {"student_id": 1, "segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_adaptation_event(self):
        """Test that handler processes adaptation events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = SimpleEventHandler(mock_db)
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "adaptation"
        event.payload = {"student_id": 1, "segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_raises_error_for_complex_event_type(self):
        """Test that handler raises ValueError for complex event types."""
        mock_db = MagicMock()

        handler = SimpleEventHandler(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        with pytest.raises(ValueError, match="not a simple event type"):
            await handler.handle(event)

    @pytest.mark.asyncio
    async def test_raises_error_for_hint_used_event(self):
        """Test that handler raises ValueError for hint_used events."""
        mock_db = MagicMock()

        handler = SimpleEventHandler(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "hint_used"
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        with pytest.raises(ValueError, match="not a simple event type"):
            await handler.handle(event)
