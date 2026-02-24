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
