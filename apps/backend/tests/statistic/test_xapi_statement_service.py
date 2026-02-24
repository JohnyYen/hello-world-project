"""
Unit tests for XAPIStatementService.

This test suite verifies:
- Statement parsing from xAPI format
- Game-specific field extraction
- Single and batch statement saving
- Statement retrieval with filters
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from src.statistic.application.service.xapi_statement_service import (
    XAPIStatementService,
)
from src.statistic.api.v1.schemas.xapi_statement import (
    XAPIStatementCreate,
    XAPIActor,
    XAPIVerb,
    XAPIActivity,
)


class TestXAPIStatementServiceInitialization:
    """Test suite for XAPIStatementService initialization."""

    def test_init_creates_instance(self):
        """Test that XAPIStatementService can be instantiated with db session."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        assert service is not None
        assert service.db == mock_db
        assert service.repository is not None


class TestXAPIStatementServiceParseStatement:
    """Test suite for statement parsing."""

    def test_parse_statement_extracts_actor_account(self, sample_xapi_statement_dict):
        """Test that actor account name is extracted correctly."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["actor_account_name"] == "123"
        assert parsed["actor_account_homepage"] == "hello-world-game"

    def test_parse_statement_extracts_verb(self, sample_xapi_statement_dict):
        """Test that verb is extracted correctly."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["verb_id"] == "http://adlnet.gov/expapi/verbs/completed"
        assert parsed["verb_display"] == {"en-US": "completed"}

    def test_parse_statement_extracts_object(self, sample_xapi_statement_dict):
        """Test that object is extracted correctly."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["object_id"] == "hello-world://segment/level_1_seg_3"
        assert (
            parsed["object_definition_type"]
            == "http://adlnet.gov/expapi/activities/lesson"
        )

    def test_parse_statement_extracts_result(self, sample_xapi_statement_dict):
        """Test that result is extracted correctly."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        # Note: float values are converted to string with decimal point
        assert parsed["result_score_raw"] == "85.0"
        assert parsed["result_score_min"] == "0.0"
        assert parsed["result_score_max"] == "100.0"
        assert parsed["result_score_scaled"] == "0.85"
        assert parsed["result_success"] is True
        assert parsed["result_completion"] is True
        assert parsed["result_duration"] == "PT5M30S"

    def test_parse_statement_extracts_context(self, sample_xapi_statement_dict):
        """Test that context is extracted correctly."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["platform"] == "Hello World Game v1.0"
        assert parsed["language"] == "es"
        assert parsed["context_extensions"] is not None

    def test_parse_statement_extracts_game_ids_from_extensions(
        self, sample_xapi_statement_dict
    ):
        """Test that game-specific IDs are extracted from context extensions."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement = XAPIStatementCreate(**sample_xapi_statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["student_id"] == 123
        assert parsed["game_id"] == 1
        assert parsed["level_id"] == 1
        assert parsed["segment_id"] == 3

    def test_parse_statement_generates_uuid(self):
        """Test that UUID is generated if not provided."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        # Create statement without id
        statement_dict = {
            "actor": {"account": {"homePage": "game", "name": "1"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed"},
            "object": {"id": "hello-world://level/1"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["id"] is not None
        assert len(parsed["id"]) == 36  # UUID format

    def test_parse_statement_handles_mbox(self):
        """Test parsing statement with mbox instead of account."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement_dict = {
            "actor": {"mbox": "mailto:test@example.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/initialized"},
            "object": {"id": "hello-world://level/1"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["actor_mbox"] == "mailto:test@example.com"
        assert parsed["actor_account_name"] is None


class TestXAPIStatementServiceParseObjectId:
    """Test suite for object ID parsing."""

    def test_parse_segment_object_id(self):
        """Test parsing segment format: hello-world://segment/level_X_seg_Y"""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement_dict = {
            "actor": {"account": {"homePage": "game", "name": "1"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed"},
            "object": {"id": "hello-world://segment/level_5_seg_10"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["level_id"] == 5
        assert parsed["segment_id"] == 10

    def test_parse_level_object_id(self):
        """Test parsing level format: hello-world://level/X"""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement_dict = {
            "actor": {"account": {"homePage": "game", "name": "1"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/passed"},
            "object": {"id": "hello-world://level/3"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["level_id"] == 3


class TestXAPIStatementServiceSave:
    """Test suite for save methods."""

    @pytest.mark.asyncio
    async def test_save_statement_calls_repository(
        self, sample_xapi_statement_dict, mock_xapi_statement
    ):
        """Test that save_statement calls repository create method."""
        mock_db = MagicMock()

        with patch.object(XAPIStatementService, "_parse_statement") as mock_parse:
            mock_parse.return_value = {"id": "test-id", "statement": {}}

            service = XAPIStatementService(db=mock_db)
            service.repository = MagicMock()
            service.repository.create = AsyncMock(return_value=mock_xapi_statement)

            statement = XAPIStatementCreate(**sample_xapi_statement_dict)
            result = await service.save_statement(statement)

            service.repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_batch_parses_all_statements(self, sample_xapi_statement_dict):
        """Test that save_batch parses all statements."""
        mock_db = MagicMock()

        with patch.object(XAPIStatementService, "_parse_statement") as mock_parse:
            mock_parse.return_value = {"id": "test-id", "statement": {}}

            service = XAPIStatementService(db=mock_db)
            service.repository = MagicMock()
            service.repository.create_batch = AsyncMock(return_value=[])

            statements = [
                XAPIStatementCreate(**sample_xapi_statement_dict),
                XAPIStatementCreate(**sample_xapi_statement_dict),
            ]
            await service.save_batch(statements)

            assert mock_parse.call_count == 2


class TestXAPIStatementServiceGet:
    """Test suite for get methods."""

    @pytest.mark.asyncio
    async def test_get_statement_calls_repository(self, mock_xapi_statement):
        """Test that get_statement calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_by_statement_id = AsyncMock(
            return_value=mock_xapi_statement
        )

        result = await service.get_statement("test-id")

        service.repository.get_by_statement_id.assert_called_once_with("test-id")

    @pytest.mark.asyncio
    async def test_get_statements_calls_repository(self, mock_xapi_statement):
        """Test that get_statements calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_all = AsyncMock(return_value=[mock_xapi_statement])

        result = await service.get_statements(skip=0, limit=100)

        service.repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_student_calls_repository(self, mock_xapi_statement):
        """Test that get_by_student calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_by_student_id = AsyncMock(
            return_value=[mock_xapi_statement]
        )

        result = await service.get_by_student(123, skip=0, limit=100)

        service.repository.get_by_student_id.assert_called_once_with(
            student_id=123, skip=0, limit=100
        )

    @pytest.mark.asyncio
    async def test_get_by_verb_calls_repository(self, mock_xapi_statement):
        """Test that get_by_verb calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_by_verb = AsyncMock(return_value=[mock_xapi_statement])

        result = await service.get_by_verb("http://adlnet.gov/expapi/verbs/completed")

        service.repository.get_by_verb.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_game_calls_repository(self, mock_xapi_statement):
        """Test that get_by_game calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_by_game_id = AsyncMock(
            return_value=[mock_xapi_statement]
        )

        result = await service.get_by_game(1)

        service.repository.get_by_game_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_level_calls_repository(self, mock_xapi_statement):
        """Test that get_by_level calls repository."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)
        service.repository = MagicMock()
        service.repository.get_by_level_id = AsyncMock(
            return_value=[mock_xapi_statement]
        )

        result = await service.get_by_level(1)

        service.repository.get_by_level_id.assert_called_once()


class TestXAPIStatementServiceEdgeCases:
    """Test suite for edge cases."""

    def test_parse_statement_handles_missing_result(self):
        """Test parsing statement without result field."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement_dict = {
            "actor": {"account": {"homePage": "game", "name": "1"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/initialized"},
            "object": {"id": "hello-world://level/1"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["result_success"] is None
        assert parsed["result_score_raw"] is None

    def test_parse_statement_handles_missing_context(self):
        """Test parsing statement without context field."""
        mock_db = MagicMock()
        service = XAPIStatementService(db=mock_db)

        statement_dict = {
            "actor": {"account": {"homePage": "game", "name": "1"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/initialized"},
            "object": {"id": "hello-world://level/1"},
        }
        statement = XAPIStatementCreate(**statement_dict)
        parsed = service._parse_statement(statement)

        assert parsed["platform"] is None
        assert parsed["language"] is None
        assert parsed["student_id"] == 1
