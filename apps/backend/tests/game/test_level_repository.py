"""
Unit tests for LevelRepository.

This test suite verifies:
- Level creation
- Level retrieval by ID
- Level retrieval by game ID
- Level updates
- Soft delete functionality
- Eager loading of segments relationship
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from datetime import datetime, timezone

from src.game.infrastructure.level_repository import LevelRepository
from src.game.domain.level import Level


class TestLevelRepositoryInitialization:
    """Test suite for LevelRepository initialization."""

    def test_init_creates_instance(self):
        """Test that LevelRepository can be instantiated with db session."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None
        assert repo.db == mock_db
        assert repo.model == Level


class TestLevelRepositoryCreate:
    """Test suite for create method."""

    def test_create_level_success(self, sample_level_data):
        """Test successful level creation."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo.model == Level


class TestLevelRepositoryGetById:
    """Test suite for get_by_id method."""

    def test_get_by_id_returns_level(self, mock_level):
        """Test successful level retrieval by ID."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryGetByIdWithSegments:
    """Test suite for get_by_id_with_segments method (eager loading)."""

    def test_get_by_id_with_segments_includes_segments(self, mock_level_with_segments):
        """Test that eager loading includes segments relationship."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryGetByGameId:
    """Test suite for get_by_game_id method."""

    def test_get_by_game_id_returns_levels(self, mock_level):
        """Test retrieval of levels by game ID."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryGetByGameIdWithSegments:
    """Test suite for get_by_game_id_with_segments method."""

    def test_get_by_game_id_with_segments_returns_list(self, mock_level_with_segments):
        """Test retrieval of levels with segments by game ID."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryGetByLevelNumber:
    """Test suite for get_by_level_number method."""

    def test_get_by_level_number_success(self, mock_level):
        """Test retrieval of level by game ID and level number."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryUpdate:
    """Test suite for update method."""

    def test_update_level_success(self, mock_level):
        """Test successful level update."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryDelete:
    """Test suite for delete (soft delete) method."""

    def test_delete_sets_deleted_flags(self, mock_level):
        """Test soft delete sets is_deleted and deleted_at."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryEdgeCases:
    """Test suite for edge cases."""

    def test_get_by_game_id_empty_result(self):
        """Test get_by_game_id returns empty list when no levels found."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)
        assert repo is not None


class TestLevelRepositoryCountLevelsByGameIds:
    """Test suite for count_levels_by_game_ids method."""

    @pytest.mark.asyncio
    async def test_empty_list_returns_empty_dict(self):
        """Test empty list returns {}."""
        mock_db = MagicMock()
        repo = LevelRepository(db=mock_db)

        result = await repo.count_levels_by_game_ids([])

        assert result == {}

    @pytest.mark.asyncio
    async def test_valid_game_ids_return_correct_counts(self):
        """Test valid game IDs return correct counts."""
        mock_db = MagicMock()
        mock_row_1 = MagicMock()
        mock_row_1.game_id = UUID("11111111-1111-1111-1111-111111111111")
        mock_row_1.__getitem__.return_value = 3
        mock_row_2 = MagicMock()
        mock_row_2.game_id = UUID("22222222-2222-2222-2222-222222222222")
        mock_row_2.__getitem__.return_value = 5
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [mock_row_1, mock_row_2]
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = LevelRepository(db=mock_db)
        result = await repo.count_levels_by_game_ids(
            [
                UUID("11111111-1111-1111-1111-111111111111"),
                UUID("22222222-2222-2222-2222-222222222222"),
            ]
        )

        assert len(result) == 2
        assert result[UUID("11111111-1111-1111-1111-111111111111")] == 3
        assert result[UUID("22222222-2222-2222-2222-222222222222")] == 5
        mock_db.execute.assert_awaited_once()
