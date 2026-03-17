"""
Unit tests for Complex Event Handler.

Tests verify:
- maps to xAPI correctly
- creates xAPI statement
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.handler.complex_event_handler import ComplexEventHandler
from src.sync.domain.sync_event import SyncEvent


class TestComplexEventHandler:
    """Test suite for ComplexEventHandler."""

    @pytest.mark.asyncio
    async def test_handles_error_event(self):
        """Test that handler processes error events and creates xAPI statement."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_mapper = MagicMock()
        mock_xapi_statement = MagicMock()
        mock_mapper.map = AsyncMock(return_value=mock_xapi_statement)

        mock_xapi_service = MagicMock()
        mock_xapi_service.save_statement = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = ComplexEventHandler(mock_db)
        handler.mapper = mock_mapper
        handler.xapi_service = mock_xapi_service
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "level_id": 5,
            "segment_id": 3,
            "error_message": "Invalid move",
        }
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_mapper.map.assert_called_once_with(event)
        mock_xapi_service.save_statement.assert_called_once_with(mock_xapi_statement)
        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_interaction_event(self):
        """Test that handler processes interaction events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_mapper = MagicMock()
        mock_xapi_statement = MagicMock()
        mock_mapper.map = AsyncMock(return_value=mock_xapi_statement)

        mock_xapi_service = MagicMock()
        mock_xapi_service.save_statement = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = ComplexEventHandler(mock_db)
        handler.mapper = mock_mapper
        handler.xapi_service = mock_xapi_service
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "interaction"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "level_id": 5,
            "segment_id": 3,
            "interaction_type": "button_click",
        }
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_mapper.map.assert_called_once_with(event)
        mock_xapi_service.save_statement.assert_called_once_with(mock_xapi_statement)
        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_handles_hint_used_event(self):
        """Test that handler processes hint_used events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_mapper = MagicMock()
        mock_xapi_statement = MagicMock()
        mock_mapper.map = AsyncMock(return_value=mock_xapi_statement)

        mock_xapi_service = MagicMock()
        mock_xapi_service.save_statement = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = ComplexEventHandler(mock_db)
        handler.mapper = mock_mapper
        handler.xapi_service = mock_xapi_service
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "hint_used"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "level_id": 5,
            "segment_id": 3,
            "hints_count": 2,
        }
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        mock_mapper.map.assert_called_once_with(event)
        mock_xapi_service.save_statement.assert_called_once_with(mock_xapi_statement)
        mock_progress_updater.update.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_raises_error_for_simple_event_type(self):
        """Test that handler raises ValueError for simple event types."""
        mock_db = MagicMock()

        handler = ComplexEventHandler(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        with pytest.raises(ValueError, match="not a complex event type"):
            await handler.handle(event)

    @pytest.mark.asyncio
    async def test_raises_error_for_attempt_event(self):
        """Test that handler raises ValueError for attempt events."""
        mock_db = MagicMock()

        handler = ComplexEventHandler(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        with pytest.raises(ValueError, match="not a complex event type"):
            await handler.handle(event)

    @pytest.mark.asyncio
    async def test_creates_xapi_statement_for_error(self):
        """Test that xAPI statement is created correctly for error events."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_mapper = MagicMock()
        mock_xapi_statement = MagicMock()
        mock_mapper.map = AsyncMock(return_value=mock_xapi_statement)

        mock_xapi_service = MagicMock()
        mock_xapi_service.save_statement = AsyncMock()

        mock_progress_updater = MagicMock()
        mock_progress_updater.update = AsyncMock()

        handler = ComplexEventHandler(mock_db)
        handler.mapper = mock_mapper
        handler.xapi_service = mock_xapi_service
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "level_id": 5,
            "segment_id": 3,
            "error_message": "Test error",
        }
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        result = mock_mapper.map.return_value
        mock_xapi_service.save_statement.assert_called_once_with(result)
