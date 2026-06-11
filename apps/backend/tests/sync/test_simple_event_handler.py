"""
Unit tests for Simple Event Handler.

Tests verify:
- handles level_time event
- handles attempt event
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.sync.application.handler.simple_event_handler import SimpleEventHandler
from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.service.sync_resolution_service import SyncResolutionService


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


class TestSimpleEventHandlerRefactor:
    """Test suite for SimpleEventHandler refactoring with SyncResolutionService."""

    def test_backward_compatibility(self):
        """SimpleEventHandler(db) works without resolution_service parameter."""
        mock_db = MagicMock()
        handler = SimpleEventHandler(mock_db)
        assert handler._resolution_service is not None
        assert isinstance(handler._resolution_service, SyncResolutionService)

    @pytest.mark.asyncio
    async def test_with_injected_resolution_service(self):
        """SimpleEventHandler uses injected resolution_service."""
        mock_db = MagicMock()
        mock_resolution_service = AsyncMock(spec=SyncResolutionService)
        mock_resolution_service.resolve_student_id = AsyncMock(return_value=uuid4())

        handler = SimpleEventHandler(mock_db, resolution_service=mock_resolution_service)
        assert handler._resolution_service is mock_resolution_service

        # Create a test event
        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.sync_session_id = uuid4()
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        # Verify the injected service was used
        mock_resolution_service.resolve_student_id.assert_called_once_with(event.sync_session_id)

    @pytest.mark.asyncio
    async def test_get_student_id_from_event_delegation(self):
        """_get_student_id_from_event delegates to SyncResolutionService."""
        mock_db = MagicMock()
        mock_resolution_service = AsyncMock(spec=SyncResolutionService)
        mock_student_id = uuid4()
        mock_resolution_service.resolve_student_id = AsyncMock(return_value=mock_student_id)

        handler = SimpleEventHandler(mock_db, resolution_service=mock_resolution_service)

        event = MagicMock(spec=SyncEvent)
        event.sync_session_id = uuid4()

        result = await handler._get_student_id_from_event(event)

        assert result == mock_student_id
        mock_resolution_service.resolve_student_id.assert_called_once_with(event.sync_session_id)

    @pytest.mark.asyncio
    async def test_get_student_id_from_event_returns_none(self):
        """_get_student_id_from_event returns None when resolution fails."""
        mock_db = MagicMock()
        mock_resolution_service = AsyncMock(spec=SyncResolutionService)
        mock_resolution_service.resolve_student_id = AsyncMock(return_value=None)

        handler = SimpleEventHandler(mock_db, resolution_service=mock_resolution_service)

        event = MagicMock(spec=SyncEvent)
        event.sync_session_id = uuid4()

        result = await handler._get_student_id_from_event(event)

        assert result is None
        mock_resolution_service.resolve_student_id.assert_called_once_with(event.sync_session_id)

    @pytest.mark.asyncio
    async def test_handle_with_injected_resolution_service(self):
        """Full handle() flow uses injected resolution_service."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_resolution_service = AsyncMock(spec=SyncResolutionService)
        mock_student_id = uuid4()
        mock_resolution_service.resolve_student_id = AsyncMock(return_value=mock_student_id)

        mock_progress_updater = AsyncMock()
        mock_progress_updater.update = AsyncMock()

        # Create handler with injected resolution_service
        handler = SimpleEventHandler(
            mock_db, resolution_service=mock_resolution_service
        )
        handler.progress_updater = mock_progress_updater

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.sync_session_id = uuid4()
        event.payload = {}
        event.timestamp = datetime.now(timezone.utc)

        await handler.handle(event)

        # Verify resolution_service was used
        mock_resolution_service.resolve_student_id.assert_called_once_with(event.sync_session_id)

        # Verify payload was enriched with student_id
        assert event.payload["student_id"] == mock_student_id

        # Verify progress_updater.update was called with enriched event
        mock_progress_updater.update.assert_called_once_with(event)
