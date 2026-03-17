"""
Unit tests for SyncSessionService.

This test suite verifies:
- Session creation
- Session ending
- Session retrieval by ID
- Session retrieval by instance ID
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.domain.sync_session import SyncSession
from src.shared.domain.exceptions import NotFoundException


class TestSyncSessionServiceCreate:
    """Test suite for create method."""

    @pytest.mark.asyncio
    async def test_create_session_success(self, mock_sync_session, sample_session_data):
        """Test successful session creation."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.create = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.create(instance_id=1)

        assert result is not None
        assert result.instance_id == sample_session_data["instance_id"]
        assert result.status == "active"
        mock_repo.create.assert_called_once()
        call_args = mock_repo.create.call_args[0][0]
        assert call_args["instance_id"] == 1
        assert call_args["status"] == "active"

    @pytest.mark.asyncio
    async def test_create_session_sets_start_time(self, mock_sync_session):
        """Test that create sets start_time to current time."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.create = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        await service.create(instance_id=1)

        call_args = mock_repo.create.call_args[0][0]
        assert "start_time" in call_args
        assert call_args["start_time"] is not None


class TestSyncSessionServiceEndSession:
    """Test suite for end_session method."""

    @pytest.mark.asyncio
    async def test_end_session_success(self, mock_sync_session):
        """Test successful session ending."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_sync_session)
        mock_repo.update = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.end_session(session_id=1)

        assert result is not None
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_end_session_not_found(self):
        """Test that ending non-existent session raises NotFoundException."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=None)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        with pytest.raises(NotFoundException):
            await service.end_session(session_id=999)

    @pytest.mark.asyncio
    async def test_end_session_sets_completed_status(self, mock_sync_session):
        """Test that ending session sets status to completed."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_sync_session)
        mock_repo.update = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        await service.end_session(session_id=1)

        call_args = mock_repo.update.call_args
        assert call_args[0][1]["status"] == "completed"
        assert "end_time" in call_args[0][1]


class TestSyncSessionServiceGetSession:
    """Test suite for get_session method."""

    @pytest.mark.asyncio
    async def test_get_session_returns_session(self, mock_sync_session):
        """Test successful session retrieval by ID."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.get_session(session_id=1)

        assert result is not None
        assert result.id == mock_sync_session.id
        mock_repo.get_by_id.assert_called_once_with(1, include_deleted=False)

    @pytest.mark.asyncio
    async def test_get_session_returns_none_when_not_found(self):
        """Test that get_session returns None when session doesn't exist."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=None)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.get_session(session_id=999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_session_with_include_deleted(self, mock_sync_session):
        """Test get_session with include_deleted parameter."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_sync_session)

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        await service.get_session(session_id=1, include_deleted=True)

        mock_repo.get_by_id.assert_called_once_with(1, include_deleted=True)


class TestSyncSessionServiceGetByInstance:
    """Test suite for get_by_instance method."""

    @pytest.mark.asyncio
    async def test_get_by_instance_returns_sessions(self, mock_sync_session):
        """Test successful retrieval of sessions by instance ID."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_session])

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.get_by_instance(instance_id=1)

        assert len(result) == 1
        assert result[0].instance_id == 1
        mock_repo.get_by_filters.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_instance_returns_empty_list_when_none(self):
        """Test that get_by_instance returns empty list when no sessions found."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[])

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        result = await service.get_by_instance(instance_id=999)

        assert result == []

    @pytest.mark.asyncio
    async def test_get_by_instance_orders_by_start_time_desc(self, mock_sync_session):
        """Test that sessions are ordered by start_time descending."""
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_by_filters = AsyncMock(return_value=[mock_sync_session])

        service = SyncSessionService(mock_db)
        service.repository = mock_repo

        await service.get_by_instance(instance_id=1)

        call_kwargs = mock_repo.get_by_filters.call_args[1]
        assert call_kwargs["order_by"] == "start_time"
        assert call_kwargs["descending"] is True
