"""
Unit tests for Pipeline Service.

Tests verify:
- process_event routes to correct handler
- Simple event goes to simple handler
- Complex event goes to complex handler
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.service.sync_to_stats_pipeline_service import (
    SyncToStatsPipelineService,
)
from src.sync.domain.sync_event import SyncEvent


class TestPipelineServiceProcessEvent:
    """Test suite for process_event() method."""

    @pytest.mark.asyncio
    async def test_process_simple_event_routes_to_simple_handler(self):
        """Test that simple events are routed to SimpleEventHandler."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        result = await service.process_event(event)

        assert result is True
        mock_simple_handler.handle.assert_called_once_with(event)
        mock_complex_handler.handle.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_complex_event_routes_to_complex_handler(self):
        """Test that complex events are routed to ComplexEventHandler."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        result = await service.process_event(event)

        assert result is True
        mock_complex_handler.handle.assert_called_once_with(event)
        mock_simple_handler.handle.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_event_routes_attempt_to_simple_handler(self):
        """Test that 'attempt' events go to simple handler."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        result = await service.process_event(event)

        assert result is True
        mock_simple_handler.handle.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_process_event_routes_hint_used_to_complex_handler(self):
        """Test that 'hint_used' events go to complex handler."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "hint_used"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        result = await service.process_event(event)

        assert result is True
        mock_complex_handler.handle.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_process_invalid_event_sends_to_dead_letter(self):
        """Test that invalid event types are sent to dead letter handler."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "invalid_event_type"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        result = await service.process_event(event)

        assert result is False
        mock_dead_letter_handler.handle.assert_called_once()
        mock_simple_handler.handle.assert_not_called()
        mock_complex_handler.handle.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_event_updates_status_to_processed(self):
        """Test that successful processing updates event status."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.status = "pending"
        event.timestamp = datetime.now(timezone.utc)

        await service.process_event(event)

        assert event.status == "processed"
        mock_db.commit.assert_called()


class TestPipelineServiceProcessBatch:
    """Test suite for process_batch() method."""

    @pytest.mark.asyncio
    async def test_process_batch_returns_summary(self):
        """Test that process_batch returns success/failure counts."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock()

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        events = [
            MagicMock(
                spec=SyncEvent,
                id=1,
                event_type="level_time",
                status="pending",
                timestamp=datetime.now(timezone.utc),
            ),
            MagicMock(
                spec=SyncEvent,
                id=2,
                event_type="attempt",
                status="pending",
                timestamp=datetime.now(timezone.utc),
            ),
            MagicMock(
                spec=SyncEvent,
                id=3,
                event_type="error",
                status="pending",
                timestamp=datetime.now(timezone.utc),
            ),
        ]

        result = await service.process_batch(events)

        assert result["total"] == 3
        assert result["successful"] == 3
        assert result["failed"] == 0

    @pytest.mark.asyncio
    async def test_process_batch_handles_failures(self):
        """Test that process_batch counts failures correctly."""
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_simple_handler = MagicMock()
        mock_simple_handler.handle = AsyncMock()

        mock_complex_handler = MagicMock()
        mock_complex_handler.handle = AsyncMock(side_effect=Exception("Handler error"))

        mock_dead_letter_handler = MagicMock()
        mock_dead_letter_handler.handle = AsyncMock()

        service = SyncToStatsPipelineService(mock_db)
        service.simple_handler = mock_simple_handler
        service.complex_handler = mock_complex_handler
        service.dead_letter_handler = mock_dead_letter_handler

        events = [
            MagicMock(
                spec=SyncEvent,
                id=1,
                event_type="level_time",
                status="pending",
                timestamp=datetime.now(timezone.utc),
            ),
            MagicMock(
                spec=SyncEvent,
                id=2,
                event_type="error",
                status="pending",
                timestamp=datetime.now(timezone.utc),
            ),
        ]

        result = await service.process_batch(events)

        assert result["total"] == 2
        assert result["successful"] == 1
        assert result["failed"] == 1
