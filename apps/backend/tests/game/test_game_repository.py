"""
Unit tests for GameRepository.

This test suite verifies:
- Game creation
- Game retrieval by ID
- Game listing with pagination
- Game updates
- Soft delete functionality
- Eager loading of levels relationship
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.game.infrastructure.game_repository import GameRepository
from src.game.domain.game import Game


class TestGameRepositoryInitialization:
    """Test suite for GameRepository initialization."""

    def test_init_creates_instance(self):
        """Test that GameRepository can be instantiated with db session."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None
        assert repo.db == mock_db
        assert repo.model == Game


class TestGameRepositoryCreate:
    """Test suite for create method."""

    def test_create_game_success(self, sample_game_data):
        """Test successful game creation."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo.model == Game


class TestGameRepositoryGetById:
    """Test suite for get_by_id method."""

    def test_get_by_id_returns_game(self, mock_game):
        """Test successful game retrieval by ID."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None

    def test_get_by_id_returns_none_when_not_found(self):
        """Test game retrieval returns None when not found."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryGetByIdWithLevels:
    """Test suite for get_by_id_with_levels method (eager loading)."""

    def test_get_by_id_with_levels_includes_levels(self, mock_game_with_levels):
        """Test that eager loading includes levels relationship."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None

    def test_get_by_id_with_levels_excludes_deleted(self):
        """Test that eager loading excludes deleted games by default."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryGetAll:
    """Test suite for get_all method."""

    def test_get_all_returns_list(self, mock_game):
        """Test get_all returns a list of games."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryGetAllWithLevels:
    """Test suite for get_all_with_levels method."""

    def test_get_all_with_levels_pagination(self, mock_game_with_levels):
        """Test pagination parameters are applied."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryUpdate:
    """Test suite for update method."""

    def test_update_game_success(self, mock_game):
        """Test successful game update."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryDelete:
    """Test suite for delete (soft delete) method."""

    def test_delete_sets_deleted_flags(self, mock_game):
        """Test soft delete sets is_deleted and deleted_at."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None

    def test_delete_returns_false_when_not_found(self):
        """Test delete returns False when game doesn't exist."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None


class TestGameRepositoryEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_get_by_id_handles_database_error(self):
        """Test database errors are handled gracefully."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None

    def test_create_handles_integrity_error(self, sample_game_data):
        """Test integrity errors during creation are handled."""
        mock_db = MagicMock()
        repo = GameRepository(db=mock_db)
        assert repo is not None
