# xAPI-specific test fixtures and configuration
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

from src.statistic.domain.xapi_statement import XAPIStatement


# ============== xAPI Statement Fixtures ==============


@pytest.fixture
def sample_xapi_statement_data():
    """Provide valid test xAPI statement data."""
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "actor_mbox": None,
        "actor_account_name": "123",
        "actor_account_homepage": "hello-world-game",
        "verb_id": "http://adlnet.gov/expapi/verbs/completed",
        "verb_display": {"en-US": "completed"},
        "object_id": "hello-world://segment/level_1_seg_3",
        "object_type": "Activity",
        "object_definition_type": "http://adlnet.gov/expapi/activities/lesson",
        "object_definition_name": {"es": "Segmento 3 - Variables"},
        "platform": "Hello World Game v1.0",
        "language": "es",
        "context_extensions": {
            "http://hello-world-game.com/extensions/game_id": 1,
            "http://hello-world-game.com/extensions/level_id": 1,
            "http://hello-world-game.com/extensions/segment_id": 3,
        },
        "result_score_raw": "85",
        "result_score_min": "0",
        "result_score_max": "100",
        "result_score_scaled": "0.85",
        "result_success": True,
        "result_completion": True,
        "result_duration": "PT5M30S",
        "result_response": None,
        "result_extensions": None,
        "timestamp": datetime.now(timezone.utc),
        "stored": datetime.now(timezone.utc),
        "statement": {
            "actor": {"account": {"homePage": "hello-world-game", "name": "123"}},
            "verb": {
                "id": "http://adlnet.gov/expapi/verbs/completed",
                "display": {"en-US": "completed"},
            },
            "object": {
                "id": "hello-world://segment/level_1_seg_3",
                "definition": {"type": "http://adlnet.gov/expapi/activities/lesson"},
            },
        },
        "student_id": 123,
        "game_id": 1,
        "level_id": 1,
        "segment_id": 3,
    }


@pytest.fixture
def mock_xapi_statement(sample_xapi_statement_data):
    """Create a mock XAPIStatement object."""
    statement = MagicMock(spec=XAPIStatement)
    statement.id = sample_xapi_statement_data["id"]
    statement.actor_mbox = sample_xapi_statement_data["actor_mbox"]
    statement.actor_account_name = sample_xapi_statement_data["actor_account_name"]
    statement.actor_account_homepage = sample_xapi_statement_data[
        "actor_account_homepage"
    ]
    statement.verb_id = sample_xapi_statement_data["verb_id"]
    statement.verb_display = sample_xapi_statement_data["verb_display"]
    statement.object_id = sample_xapi_statement_data["object_id"]
    statement.object_type = sample_xapi_statement_data["object_type"]
    statement.object_definition_type = sample_xapi_statement_data[
        "object_definition_type"
    ]
    statement.object_definition_name = sample_xapi_statement_data[
        "object_definition_name"
    ]
    statement.platform = sample_xapi_statement_data["platform"]
    statement.language = sample_xapi_statement_data["language"]
    statement.context_extensions = sample_xapi_statement_data["context_extensions"]
    statement.result_score_raw = sample_xapi_statement_data["result_score_raw"]
    statement.result_score_min = sample_xapi_statement_data["result_score_min"]
    statement.result_score_max = sample_xapi_statement_data["result_score_max"]
    statement.result_score_scaled = sample_xapi_statement_data["result_score_scaled"]
    statement.result_success = sample_xapi_statement_data["result_success"]
    statement.result_completion = sample_xapi_statement_data["result_completion"]
    statement.result_duration = sample_xapi_statement_data["result_duration"]
    statement.timestamp = sample_xapi_statement_data["timestamp"]
    statement.stored = sample_xapi_statement_data["stored"]
    statement.statement = sample_xapi_statement_data["statement"]
    statement.student_id = sample_xapi_statement_data["student_id"]
    statement.game_id = sample_xapi_statement_data["game_id"]
    statement.level_id = sample_xapi_statement_data["level_id"]
    statement.segment_id = sample_xapi_statement_data["segment_id"]
    return statement


@pytest.fixture
def sample_xapi_statement_dict():
    """Provide a sample xAPI statement dict for service testing."""
    return {
        "actor": {"account": {"homePage": "hello-world-game", "name": "123"}},
        "verb": {
            "id": "http://adlnet.gov/expapi/verbs/completed",
            "display": {"en-US": "completed"},
        },
        "object": {
            "id": "hello-world://segment/level_1_seg_3",
            "definition": {
                "type": "http://adlnet.gov/expapi/activities/lesson",
                "name": {"es": "Segmento 3"},
            },
        },
        "result": {
            "score": {"raw": 85, "min": 0, "max": 100, "scaled": 0.85},
            "success": True,
            "completion": True,
            "duration": "PT5M30S",
        },
        "context": {
            "platform": "Hello World Game v1.0",
            "language": "es",
            "extensions": {
                "http://hello-world-game.com/extensions/game_id": 1,
                "http://hello-world-game.com/extensions/level_id": 1,
                "http://hello-world-game.com/extensions/segment_id": 3,
            },
        },
        "timestamp": "2026-02-13T10:30:00Z",
    }


@pytest.fixture
def sample_xapi_passed_statement():
    """Provide a sample xAPI passed statement."""
    return {
        "actor": {"account": {"homePage": "hello-world-game", "name": "456"}},
        "verb": {"id": "http://adlnet.gov/expapi/verbs/passed"},
        "object": {"id": "hello-world://level/2"},
        "result": {
            "score": {"raw": 90, "min": 0, "max": 100},
            "success": True,
            "completion": True,
        },
        "context": {
            "platform": "Hello World Game v1.0",
            "extensions": {
                "http://hello-world-game.com/extensions/game_id": 1,
                "http://hello-world-game.com/extensions/level_id": 2,
            },
        },
    }


@pytest.fixture
def sample_xapi_failed_statement():
    """Provide a sample xAPI failed statement."""
    return {
        "actor": {"account": {"homePage": "hello-world-game", "name": "789"}},
        "verb": {"id": "http://adlnet.gov/expapi/verbs/failed"},
        "object": {"id": "hello-world://segment/level_1_seg_2"},
        "result": {"success": False, "completion": True},
        "context": {
            "platform": "Hello World Game v1.0",
            "extensions": {
                "http://hello-world-game.com/extensions/game_id": 1,
                "http://hello-world-game.com/extensions/level_id": 1,
                "http://hello-world-game.com/extensions/segment_id": 2,
            },
        },
    }


@pytest.fixture
def mock_xapi_repository():
    """Create a mock XAPIStatementRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_statement_id = AsyncMock()
    repo.get_by_actor = AsyncMock()
    repo.get_by_student_id = AsyncMock()
    repo.get_by_verb = AsyncMock()
    repo.get_by_object = AsyncMock()
    repo.get_by_game_id = AsyncMock()
    repo.get_by_level_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.create_batch = AsyncMock()
    repo.count = AsyncMock()
    return repo
