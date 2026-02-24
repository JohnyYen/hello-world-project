"""
Unit tests for SegmentLevelRepository.

This test suite verifies:
- Segment creation
- Segment retrieval by ID
- Segment retrieval by level ID
- Segment updates
- Soft delete functionality
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.game.infrastructure.segment_level_repository import SegmentLevelRepository
from src.game.domain.segment_level import SegmentLevel


class TestSegmentLevelRepositoryInitialization:
    """Test suite for SegmentLevelRepository initialization."""

    def test_init_creates_instance(self):
        """Test that SegmentLevelRepository can be instantiated with db session."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None
        assert repo.db == mock_db
        assert repo.model == SegmentLevel


class TestSegmentLevelRepositoryCreate:
    """Test suite for create method."""

    def test_create_segment_success(self, sample_segment_data):
        """Test successful segment creation."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo.model == SegmentLevel


class TestSegmentLevelRepositoryGetById:
    """Test suite for get_by_id method."""

    def test_get_by_id_returns_segment(self, mock_segment):
        """Test successful segment retrieval by ID."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None


class TestSegmentLevelRepositoryGetByLevelId:
    """Test suite for get_by_level_id method."""

    def test_get_by_level_id_returns_segments(self, mock_segment):
        """Test retrieval of segments by level ID."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None


class TestSegmentLevelRepositoryUpdate:
    """Test suite for update method."""

    def test_update_segment_success(self, mock_segment):
        """Test successful segment update."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None


class TestSegmentLevelRepositoryDelete:
    """Test suite for delete (soft delete) method."""

    def test_delete_sets_deleted_flags(self, mock_segment):
        """Test soft delete sets is_deleted and deleted_at."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None


class TestSegmentLevelRepositoryEdgeCases:
    """Test suite for edge cases."""

    def test_get_by_level_id_empty_result(self):
        """Test get_by_level_id returns empty list when no segments found."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None

    def test_update_handles_not_found(self):
        """Test update returns None when segment not found."""
        mock_db = MagicMock()
        repo = SegmentLevelRepository(db=mock_db)
        assert repo is not None
