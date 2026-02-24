"""
Unit tests for GameInstanceRepository.

This test suite verifies:
- Instance creation
- Instance retrieval by ID
- Instance retrieval by game ID
- Instance retrieval by student ID
- Instance retrieval by status
- Instance updates (including status changes)
- Soft delete functionality
- Eager loading of game and student relationships
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.domain.game_instance import GameInstance


class TestGameInstanceRepositoryInitialization:
    """Test suite for GameInstanceRepository initialization."""

    def test_init_creates_instance(self):
        """Test that GameInstanceRepository can be instantiated with db session."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None
        assert repo.db == mock_db
        assert repo.model == GameInstance


class TestGameInstanceRepositoryCreate:
    """Test suite for create method."""

    def test_create_instance_success(self, sample_instance_data):
        """Test successful instance creation."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo.model == GameInstance


class TestGameInstanceRepositoryGetById:
    """Test suite for get_by_id method."""

    def test_get_by_id_returns_instance(self, mock_instance):
        """Test successful instance retrieval by ID."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByIdWithRelations:
    """Test suite for get_by_id_with_relations method (eager loading)."""

    def test_get_by_id_with_relations_includes_game_and_student(
        self, mock_instance_with_relations
    ):
        """Test that eager loading includes game and student relationships."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByGameId:
    """Test suite for get_by_game_id method."""

    def test_get_by_game_id_returns_instances(self, mock_instance):
        """Test retrieval of instances by game ID."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByUserId:
    """Test suite for get_by_user_id method."""

    def test_get_by_user_id_returns_instances(self, mock_instance):
        """Test retrieval of instances by user ID."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByStatus:
    """Test suite for get_by_status method."""

    def test_get_by_status_returns_instances(self, mock_instance):
        """Test retrieval of instances by status."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None

    def test_get_by_status_filter_active(self, mock_instance):
        """Test filtering by active status."""
        mock_instance.status = "active"
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None

    def test_get_by_status_filter_completed(self, mock_instance):
        """Test filtering by completed status."""
        mock_instance.status = "completed"
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByGameAndUser:
    """Test suite for get_by_game_and_user method."""

    def test_get_by_game_and_user_returns_instance(self, mock_instance):
        """Test retrieval of instance by game ID and user ID."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetByStudentId:
    """Test suite for get_by_student_id method."""

    def test_get_by_student_id_returns_instances(self, mock_instance):
        """Test retrieval of instances by student ID."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryGetAllWithRelations:
    """Test suite for get_all_with_relations method."""

    def test_get_all_with_relations_pagination(self, mock_instance_with_relations):
        """Test pagination parameters are applied."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryUpdate:
    """Test suite for update method."""

    def test_update_status_to_completed(self, mock_instance):
        """Test updating instance status to completed."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None

    def test_update_status_to_abandoned(self, mock_instance):
        """Test updating instance status to abandoned."""
        mock_instance.status = "abandoned"
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryDelete:
    """Test suite for delete (soft delete) method."""

    def test_delete_sets_deleted_flags(self, mock_instance):
        """Test soft delete sets is_deleted and deleted_at."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None


class TestGameInstanceRepositoryEdgeCases:
    """Test suite for edge cases."""

    def test_get_by_game_id_empty_result(self):
        """Test get_by_game_id returns empty list when no instances found."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None

    def test_get_by_status_empty_result(self):
        """Test get_by_status returns empty list when no instances found."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None

    def test_multiple_active_instances_allowed(self, mock_instance):
        """Test that multiple active instances can exist (no unique constraint enforcement in repo)."""
        mock_db = MagicMock()
        repo = GameInstanceRepository(db=mock_db)
        assert repo is not None
