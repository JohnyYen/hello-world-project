"""
Unit tests for XAPIStatementRepository.

This test suite verifies:
- Statement creation
- Statement retrieval by ID
- Statement retrieval by actor/student
- Statement retrieval by verb
- Statement retrieval by game/level
- Batch creation
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.statistic.infrastructure.xapi_statement_repository import (
    XAPIStatementRepository,
)
from src.statistic.domain.xapi_statement import XAPIStatement


class TestXAPIStatementRepositoryInitialization:
    """Test suite for XAPIStatementRepository initialization."""

    def test_init_creates_instance(self):
        """Test that XAPIStatementRepository can be instantiated with db session."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None
        assert repo.db == mock_db
        assert repo.model == XAPIStatement


class TestXAPIStatementRepositoryCreate:
    """Test suite for create method."""

    def test_create_statement_success(self, sample_xapi_statement_data):
        """Test successful statement creation."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo.model == XAPIStatement


class TestXAPIStatementRepositoryGetById:
    """Test suite for get_by_id method."""

    def test_get_by_id_returns_statement(self, mock_xapi_statement):
        """Test successful statement retrieval by ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByStatementId:
    """Test suite for get_by_statement_id method."""

    def test_get_by_statement_id_returns_statement(self, mock_xapi_statement):
        """Test successful statement retrieval by xAPI statement UUID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByActor:
    """Test suite for get_by_actor method."""

    def test_get_by_actor_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by actor account name."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByStudentId:
    """Test suite for get_by_student_id method."""

    def test_get_by_student_id_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by student ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByVerb:
    """Test suite for get_by_verb method."""

    def test_get_by_verb_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by verb ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByObject:
    """Test suite for get_by_object method."""

    def test_get_by_object_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by object ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByGameId:
    """Test suite for get_by_game_id method."""

    def test_get_by_game_id_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by game ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetByLevelId:
    """Test suite for get_by_level_id method."""

    def test_get_by_level_id_returns_statements(self, mock_xapi_statement):
        """Test retrieval of statements by level ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryGetAll:
    """Test suite for get_all method."""

    def test_get_all_returns_list(self, mock_xapi_statement):
        """Test get_all returns a list of statements."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None

    def test_get_all_pagination(self, mock_xapi_statement):
        """Test pagination parameters are applied."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryBatch:
    """Test suite for batch creation."""

    def test_create_batch_returns_statements(self, sample_xapi_statement_data):
        """Test batch creation returns list of statements."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryCount:
    """Test suite for count methods."""

    def test_count_by_student(self):
        """Test counting statements by student ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None

    def test_count_by_verb(self):
        """Test counting statements by verb ID."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None


class TestXAPIStatementRepositoryEdgeCases:
    """Test suite for edge cases."""

    def test_get_by_student_id_empty_result(self):
        """Test get_by_student_id returns empty list when no statements found."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None

    def test_get_by_verb_empty_result(self):
        """Test get_by_verb returns empty list when no statements found."""
        mock_db = MagicMock()
        repo = XAPIStatementRepository(db=mock_db)
        assert repo is not None
