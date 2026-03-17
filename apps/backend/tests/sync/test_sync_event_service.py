"""
Unit tests for SyncEventService.

This test suite verifies:
- Single event creation
- Batch event creation
- Event retrieval by session ID
- Event validation (session existence)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.service.sync_event_service import SyncEventService
from src.sync.domain.sync_event import SyncEvent
from src.sync.api.v1.schemas.sync_event import SyncEventCreate
from src.shared.domain.exceptions import NotFoundException


class TestSyncEventServiceCreate:
    """Test suite for create method."""

    @pytest.mark.asyncio
    async def test_create_event_success(self, mock_sync_event, sample_event_data):
        """Test successful event creation."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.create = AsyncMock(return_value=mock_sync_event)

        mock_session_repo = MagicMock()
        mock_session_repo.exists = AsyncMock(return_value=True)

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        event_data = SyncEventCreate(**sample_event_data)
        result = await service.create(event_data=event_data)

        assert result is not None
        assert result.event_type == sample_event_data["event_type"]
        mock_session_repo.exists.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_create_event_validates_session_exists(self, sample_event_data):
        """Test that creating event with invalid session raises NotFoundException."""
        mock_db = MagicMock()
        mock_repo = MagicMock()

        mock_session_repo = MagicMock()
        mock_session_repo.exists = AsyncMock(return_value=False)

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        event_data = SyncEventCreate(**sample_event_data)

        with pytest.raises(NotFoundException):
            await service.create(event_data=event_data)

    @pytest.mark.asyncio
    async def test_create_event_sets_timestamp(
        self, mock_sync_event, sample_event_data
    ):
        """Test that create sets timestamp to current time."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.create = AsyncMock(return_value=mock_sync_event)

        mock_session_repo = MagicMock()
        mock_session_repo.exists = AsyncMock(return_value=True)

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        event_data = SyncEventCreate(**sample_event_data)
        await service.create(event_data=event_data)

        call_args = mock_repo.create.call_args[0][0]
        assert "timestamp" in call_args
        assert call_args["status"] == "pending"


class TestSyncEventServiceCreateBatch:
    """Test suite for create_batch method."""

    @pytest.mark.asyncio
    async def test_create_batch_events_success(
        self, mock_sync_event, sample_event_data
    ):
        """Test successful batch event creation."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.create = AsyncMock(side_effect=[mock_sync_event, mock_sync_event])

        mock_session_repo = MagicMock()
        mock_session_repo.exists = AsyncMock(return_value=True)

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        events_data = [
            SyncEventCreate(**sample_event_data),
            SyncEventCreate(**sample_event_data),
        ]
        result = await service.create_batch(events_data)

        assert len(result) == 2
        mock_repo.create.call_count == 2

    @pytest.mark.asyncio
    async def test_create_batch_empty_list(self):
        """Test that create_batch returns empty list for empty input."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_session_repo = MagicMock()

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        result = await service.create_batch([])

        assert result == []
        mock_repo.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_batch_validates_all_sessions(self, sample_event_data):
        """Test that batch creation validates all unique session IDs."""
        mock_db = MagicMock()
        mock_repo = MagicMock()

        mock_session_repo = MagicMock()
        mock_session_repo.exists = AsyncMock(return_value=False)

        service = SyncEventService(mock_db)
        service.repository = mock_repo
        service.session_repository = mock_session_repo

        events_data = [
            SyncEventCreate(**sample_event_data),
            SyncEventCreate(sync_session_id=2, event_type="test", payload={}),
        ]

        with pytest.raises(NotFoundException):
            await service.create_batch(events_data)


class TestSyncEventServiceGetBySession:
    """Test suite for get_by_session method."""

    @pytest.mark.asyncio
    async def test_get_by_session_returns_events(self, mock_sync_event):
        """Test successful retrieval of events by session ID."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_event])

        service = SyncEventService(mock_db)
        service.repository = mock_repo

        result = await service.get_by_session(session_id=1)

        assert len(result) == 1
        assert result[0].sync_session_id == 1
        mock_repo.get_by_filters.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_session_returns_empty_list_when_none(self):
        """Test that get_by_session returns empty list when no events found."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[])

        service = SyncEventService(mock_db)
        service.repository = mock_repo

        result = await service.get_by_session(session_id=999)

        assert result == []

    @pytest.mark.asyncio
    async def test_get_by_session_orders_by_timestamp_desc(self, mock_sync_event):
        """Test that events are ordered by timestamp descending."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_event])

        service = SyncEventService(mock_db)
        service.repository = mock_repo

        await service.get_by_session(session_id=1)

        call_kwargs = mock_repo.get_by_filters.call_args[1]
        assert call_kwargs["order_by"] == "timestamp"
        assert call_kwargs["descending"] is True


class TestSyncEventServiceGetEventsBySession:
    """Test suite for get_events_by_session method."""

    @pytest.mark.asyncio
    async def test_get_events_by_session_with_type_filter(self, mock_sync_event):
        """Test event retrieval with optional type filter."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_event])

        service = SyncEventService(mock_db)
        service.repository = mock_repo

        result = await service.get_events_by_session(
            session_id=1, event_type="player_action"
        )

        call_kwargs = mock_repo.get_by_filters.call_args[1]
        assert call_kwargs["filters"]["event_type"] == "player_action"

    @pytest.mark.asyncio
    async def test_get_events_by_session_without_type_filter(self, mock_sync_event):
        """Test event retrieval without type filter."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_event])

        service = SyncEventService(mock_db)
        service.repository = mock_repo

        result = await service.get_events_by_session(session_id=1)

        call_kwargs = mock_repo.get_by_filters.call_args[1]
        assert "event_type" not in call_kwargs["filters"]
