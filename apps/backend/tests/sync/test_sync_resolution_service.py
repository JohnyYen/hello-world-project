"""
Tests for SyncResolutionService.

Tests verify the chain traversal:
  SyncSession -> GameInstance -> Level -> SegmentLevel

Uses mocked AsyncSession to avoid database dependency.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.service.sync_resolution_service import SyncResolutionService


class TestResolveStudentId:
    """Tests for SyncResolutionService.resolve_student_id()."""

    @pytest.mark.asyncio
    async def test_resolves_student_id_from_session_chain(self):
        sync_session_id = uuid4()
        student_id = uuid4()
        game_instance_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.student_id = student_id
        mock_game_instance.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(side_effect=[mock_result_sync, mock_result_gi])

        service = SyncResolutionService(mock_db)
        result = await service.resolve_student_id(sync_session_id)

        assert result == student_id
        assert mock_db.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_returns_none_when_sync_session_not_found(self):
        sync_session_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(return_value=mock_result)

        service = SyncResolutionService(mock_db)
        result = await service.resolve_student_id(sync_session_id)

        assert result is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_none_when_game_instance_not_found(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(side_effect=[mock_result_sync, mock_result_gi])

        service = SyncResolutionService(mock_db)
        result = await service.resolve_student_id(sync_session_id)

        assert result is None
        assert mock_db.execute.call_count == 2

class TestResolveSegmentLevelIdFromObject:
    """Tests for SyncResolutionService.resolve_segment_level_id_from_object()."""

    @pytest.mark.asyncio
    async def test_resolves_segment_level_id_from_chain(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()
        level_id = uuid4()
        segment_level_id = uuid4()
        level_number = 5

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_level = MagicMock()
        mock_level.id = level_id
        mock_level.deleted_at = None

        mock_segment_level = MagicMock()
        mock_segment_level.id = segment_level_id
        mock_segment_level.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = mock_level

        mock_result_seg = MagicMock()
        mock_result_seg.scalar_one_or_none.return_value = mock_segment_level

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level, mock_result_seg]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_object(
            sync_session_id, level_number
        )

        assert result == segment_level_id
        assert mock_db.execute.call_count == 4

    @pytest.mark.asyncio
    async def test_returns_none_when_sync_session_not_found(self):
        sync_session_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(return_value=mock_result)

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_object(
            sync_session_id, 5
        )

        assert result is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_none_when_game_instance_not_found(self):
        sync_session_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = uuid4()
        mock_sync_session.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(side_effect=[mock_result_sync, mock_result_gi])

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_object(
            sync_session_id, 5
        )

        assert result is None
        assert mock_db.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_returns_none_when_level_not_found(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_object(
            sync_session_id, 5
        )

        assert result is None
        assert mock_db.execute.call_count == 3

    @pytest.mark.asyncio
    async def test_returns_none_when_segment_level_not_found(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()
        level_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_level = MagicMock()
        mock_level.id = level_id

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = mock_level

        mock_result_seg = MagicMock()
        mock_result_seg.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level, mock_result_seg]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_object(
            sync_session_id, 5
        )

        assert result is None
        assert mock_db.execute.call_count == 4


class TestResolveSegmentLevelIdFromSegment:
    """Tests for SyncResolutionService.resolve_segment_level_id_from_segment()."""

    @pytest.mark.asyncio
    async def test_resolves_segment_level_id_from_segment(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()
        level_id = uuid4()
        segment_level_id = uuid4()
        segment_id = 42

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_level = MagicMock()
        mock_level.id = level_id
        mock_level.deleted_at = None

        mock_segment_level = MagicMock()
        mock_segment_level.id = segment_level_id
        mock_segment_level.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = mock_level

        mock_result_seg = MagicMock()
        mock_result_seg.scalar_one_or_none.return_value = mock_segment_level

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level, mock_result_seg]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_segment(
            sync_session_id, segment_id
        )

        assert result == segment_level_id
        assert mock_db.execute.call_count == 4

    @pytest.mark.asyncio
    async def test_returns_none_when_sync_session_not_found(self):
        sync_session_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(return_value=mock_result)

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_segment(
            sync_session_id, 42
        )

        assert result is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_none_when_level_not_found_for_segment(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_segment(
            sync_session_id, 42
        )

        assert result is None
        assert mock_db.execute.call_count == 3

    @pytest.mark.asyncio
    async def test_returns_none_when_segment_level_not_found(self):
        sync_session_id = uuid4()
        game_instance_id = uuid4()
        game_id = uuid4()
        level_id = uuid4()

        mock_sync_session = MagicMock()
        mock_sync_session.instance_id = game_instance_id
        mock_sync_session.deleted_at = None

        mock_game_instance = MagicMock()
        mock_game_instance.game_id = game_id
        mock_game_instance.deleted_at = None

        mock_level = MagicMock()
        mock_level.id = level_id

        mock_result_sync = MagicMock()
        mock_result_sync.scalar_one_or_none.return_value = mock_sync_session

        mock_result_gi = MagicMock()
        mock_result_gi.scalar_one_or_none.return_value = mock_game_instance

        mock_result_level = MagicMock()
        mock_result_level.scalar_one_or_none.return_value = mock_level

        mock_result_seg = MagicMock()
        mock_result_seg.scalar_one_or_none.return_value = None

        mock_db = AsyncMock(spec=AsyncSession)
        mock_db.execute = AsyncMock(
            side_effect=[mock_result_sync, mock_result_gi, mock_result_level, mock_result_seg]
        )

        service = SyncResolutionService(mock_db)
        result = await service.resolve_segment_level_id_from_segment(
            sync_session_id, 42
        )

        assert result is None
        assert mock_db.execute.call_count == 4
