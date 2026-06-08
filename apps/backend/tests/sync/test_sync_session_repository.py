import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.infrastructure.repositories.sync_session_repository import (
    SyncSessionRepository,
)
from src.sync.domain.sync_session import SyncSession


class TestSyncSessionRepositoryEndStale:
    """Test suite for end_stale method."""

    @pytest.mark.asyncio
    async def test_end_stale_returns_affected_count(self):
        mock_db = MagicMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.rowcount = 5
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()

        repo = SyncSessionRepository(mock_db)
        count = await repo.end_stale(timedelta(hours=2))

        assert count == 5

    @pytest.mark.asyncio
    async def test_end_stale_commits_transaction(self):
        mock_db = MagicMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.rowcount = 3
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()

        repo = SyncSessionRepository(mock_db)
        await repo.end_stale(timedelta(hours=2))

        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_end_stale_returns_zero_when_none_stale(self):
        mock_db = MagicMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()

        repo = SyncSessionRepository(mock_db)
        count = await repo.end_stale(timedelta(hours=2))

        assert count == 0

    @pytest.mark.asyncio
    async def test_end_stale_calls_execute(self):
        mock_db = MagicMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()

        repo = SyncSessionRepository(mock_db)
        await repo.end_stale(timedelta(hours=2))

        mock_db.execute.assert_called_once()
