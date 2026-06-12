"""
Unit tests for Progress Updater.

Tests verify:
- increments attempt_count
- updates score
- raw_stats resolution and efficiency_rating cast
- backward compatibility
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
from uuid import uuid4

from src.sync.application.handler.progress_updater import ProgressUpdater
from src.sync.domain.service.sync_resolution_service import SyncResolutionService
from src.sync.domain.sync_event import SyncEvent
from src.statistic.domain.progress import Progress


def _make_db(execute_return_none: bool = True) -> MagicMock:
    """Create a mock db that returns None from scalar_one_or_none by default,
    making SyncResolutionService return None (triggering payload fallback)."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None if execute_return_none else MagicMock()

    mock_db = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    return mock_db


class TestProgressUpdater:
    """Test suite for ProgressUpdater."""

    @pytest.mark.asyncio
    async def test_updates_attempt_count(self):
        """Test that attempt event increments attempt_count."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.attempt_count = 5
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 10,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1] == {"attempt_count": 10}

    @pytest.mark.asyncio
    async def test_updates_efficiency_rating(self):
        """Test that score event updates efficiency_rating."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.efficiency_rating = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "score"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "rating": 85,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1] == {"efficiency_rating": 85}

    @pytest.mark.asyncio
    async def test_creates_new_progress_when_not_found(self):
        """Test that new progress is created when none exists."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_repository.get_by_student_and_segment = AsyncMock(return_value=None)
        mock_repository.create = AsyncMock()
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 5,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_called_once_with(
            student_id=1, segment_level_id=1
        )
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_updates_error_count(self):
        """Test that error event updates error_count."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.error_count = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "error"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 3,
            "details": {"error": "test error"},
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["error_count"] == 3
        assert call_args[0][1]["errors_details"] == {"error": "test error"}

    @pytest.mark.asyncio
    async def test_updates_hints_used_count(self):
        """Test that hint_used event updates hints_used_count."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.hints_used_count = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "hint_used"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 2,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["hints_used_count"] == 2

    @pytest.mark.asyncio
    async def test_updates_objectives_completed(self):
        """Test that level_completed event updates objectives_completed."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_progress.objectives_completed = 0
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_completed"
        event.payload = {
            "student_id": 1,
            "segment_level_id": 1,
            "count": 5,
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][1]["objectives_completed"] == 5

    @pytest.mark.asyncio
    async def test_handles_missing_student_id(self):
        """Test that event without student_id is handled gracefully."""
        mock_db = _make_db()

        mock_repository = MagicMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {"segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_missing_segment_level_id(self):
        """Test that event without segment_level_id is handled gracefully."""
        mock_db = _make_db()

        mock_repository = MagicMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "attempt"
        event.payload = {"student_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.get_by_student_and_segment.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_level_time_without_updates(self):
        """Test that level_time event doesn't update any fields."""
        mock_db = _make_db()

        mock_repository = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repository.get_by_student_and_segment = AsyncMock(
            return_value=mock_progress
        )
        mock_repository.update = AsyncMock()

        updater = ProgressUpdater(mock_db)
        updater.repository = mock_repository

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "level_time"
        event.payload = {"student_id": 1, "segment_level_id": 1}
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        mock_repository.update.assert_not_called()


class TestProgressUpdaterRawStats:
    """Tests for raw_stats event type resolution and handling."""

    @pytest.mark.asyncio
    async def test_raw_stats_with_valid_segment_id(self):
        """raw_stats with segment_id resolves SegmentLevel and casts efficiency to int."""
        segment_level_id = uuid4()
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)
        mock_svc.resolve_segment_level_id_from_segment = AsyncMock(
            return_value=segment_level_id
        )

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "raw_stats"
        event.sync_session_id = sync_session_id
        event.payload = {
            "segment_id": 5,
            "efficiency_rating": 85.7,
            "attempt_count": 3,
            "error_count": 1,
            "hints_used_count": 2,
            "objectives_completed": 1,
        }

        await updater.update(event)

        mock_svc.resolve_segment_level_id_from_segment.assert_called_once_with(
            sync_session_id, 5
        )
        mock_repo.update.assert_called_once()
        call_args = mock_repo.update.call_args
        assert call_args[0][1]["efficiency_rating"] == 85
        assert call_args[0][1]["attempt_count"] == 3
        assert call_args[0][1]["error_count"] == 1
        assert call_args[0][1]["hints_used_count"] == 2
        assert call_args[0][1]["objectives_completed"] == 1

    @pytest.mark.asyncio
    async def test_raw_stats_missing_segment_id(self):
        """raw_stats without segment_id returns early."""
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "raw_stats"
        event.sync_session_id = sync_session_id
        event.payload = {"efficiency_rating": 85.7}

        await updater.update(event)

        mock_repo.get_by_student_and_segment.assert_not_called()
        mock_repo.update.assert_not_called()
        mock_svc.resolve_segment_level_id_from_segment.assert_not_called()

    @pytest.mark.asyncio
    async def test_raw_stats_invalid_segment_id(self):
        """raw_stats with non-numeric segment_id returns early."""
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "raw_stats"
        event.sync_session_id = sync_session_id
        event.payload = {"segment_id": "abc", "efficiency_rating": 85.7}

        await updater.update(event)

        mock_repo.get_by_student_and_segment.assert_not_called()
        mock_repo.update.assert_not_called()
        mock_svc.resolve_segment_level_id_from_segment.assert_not_called()


class TestProgressUpdaterEfficiencyRating:
    """Tests for efficiency_rating int cast in raw_stats _build_update_data."""

    @pytest.mark.parametrize("input_val,expected", [
        (85.7, 85),
        (0.0, 0),
        (99.999, 99),
        (None, 0),
    ])
    def test_efficiency_rating_cast(self, input_val, expected):
        """efficiency_rating is cast to int for raw_stats events."""
        mock_db = MagicMock()
        updater = ProgressUpdater(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.event_type = "raw_stats"
        event.payload = {"efficiency_rating": input_val}

        result = updater._build_update_data(event)
        assert result["efficiency_rating"] == expected

    def test_efficiency_rating_default_when_missing(self):
        """efficiency_rating defaults to 0 when not in payload."""
        mock_db = MagicMock()
        updater = ProgressUpdater(mock_db)

        event = MagicMock(spec=SyncEvent)
        event.event_type = "raw_stats"
        event.payload = {}

        result = updater._build_update_data(event)
        assert result["efficiency_rating"] == 0


class TestProgressUpdaterXapiStatement:
    """Tests that xapi_statement events still use existing resolution path unchanged."""

    @pytest.mark.asyncio
    async def test_xapi_statement_uses_object_resolution(self):
        """xapi_statement with object_type/object_id uses from_object resolution."""
        segment_level_id = uuid4()
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)
        mock_svc.resolve_segment_level_id_from_object = AsyncMock(
            return_value=segment_level_id
        )

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "object_type": "activity",
            "object_id": "5",
            "result": {"score_scaled": 0.85},
        }

        await updater.update(event)

        mock_svc.resolve_segment_level_id_from_object.assert_called_once_with(
            sync_session_id, 5
        )
        mock_svc.resolve_segment_level_id_from_segment.assert_not_called()
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_xapi_statement_with_level_type(self):
        """xapi_statement with object_type='level' uses same resolution path."""
        segment_level_id = uuid4()
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)
        mock_svc.resolve_segment_level_id_from_object = AsyncMock(
            return_value=segment_level_id
        )

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "object_type": "level",
            "object_id": "3",
            "result": {"completion": True},
        }

        await updater.update(event)

        mock_svc.resolve_segment_level_id_from_object.assert_called_once_with(
            sync_session_id, 3
        )
        mock_svc.resolve_segment_level_id_from_segment.assert_not_called()
        mock_repo.update.assert_called_once()


class TestResolveLevelAndSegmentFromObjectId:
    """Tests for ProgressUpdater._resolve_level_and_segment_from_object_id()."""

    @pytest.mark.parametrize("object_id,expected", [
        ("hello-world://level/1/segment/2", (1, 2)),
        ("hello-world://level/5/segment/3", (5, 3)),
        ("5", (5, None)),
        ("hello-world://level/2", (2, None)),
        ("hello-world://segment/level_1_seg_3", (1, None)),
        ("hello-world://activity/course_1", (1, None)),
    ])
    def test_resolves_various_formats(self, object_id, expected):
        mock_db = MagicMock()
        updater = ProgressUpdater(mock_db)
        result = updater._resolve_level_and_segment_from_object_id(object_id)
        assert result == expected

    @pytest.mark.parametrize("object_id", [
        "",
        "hello-world://level/abc/segment/xyz",
        "abc",
        None,
    ])
    def test_returns_none_for_invalid(self, object_id):
        mock_db = MagicMock()
        updater = ProgressUpdater(mock_db)
        result = updater._resolve_level_and_segment_from_object_id(object_id)
        assert result is None


class TestProgressUpdaterXapiStatementCompoundURI:
    """Tests that xapi_statement events resolve compound URIs correctly."""

    @pytest.mark.asyncio
    async def test_xapi_statement_with_compound_uri(self):
        segment_level_id = uuid4()
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)
        mock_svc.resolve_segment_level_id_from_object = AsyncMock(
            return_value=segment_level_id
        )

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "object_type": "activity",
            "object_id": "hello-world://level/3/segment/7",
            "result": {"score_scaled": 0.9},
        }

        await updater.update(event)

        mock_svc.resolve_segment_level_id_from_object.assert_called_once_with(
            sync_session_id, 3, 7
        )
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_xapi_statement_legacy_object_id_falls_back(self):
        segment_level_id = uuid4()
        student_id = uuid4()
        sync_session_id = uuid4()

        mock_svc = AsyncMock(spec=SyncResolutionService)
        mock_svc.resolve_student_id = AsyncMock(return_value=student_id)
        mock_svc.resolve_segment_level_id_from_object = AsyncMock(
            return_value=segment_level_id
        )

        mock_db = MagicMock()
        mock_db.commit = AsyncMock()

        mock_repo = MagicMock()
        mock_progress = MagicMock(spec=Progress)
        mock_progress.id = 1
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()

        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo

        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "object_type": "level",
            "object_id": "hello-world://level/2",
            "result": {"completion": True},
        }

        await updater.update(event)

        mock_svc.resolve_segment_level_id_from_object.assert_called_once_with(
            sync_session_id, 2
        )
        mock_repo.update.assert_called_once()


class TestProgressUpdaterConstructor:
    """Tests for ProgressUpdater constructor backward compatibility."""

    def test_backward_compatibility(self):
        """ProgressUpdater(db) works without resolution_service parameter."""
        mock_db = MagicMock()
        updater = ProgressUpdater(mock_db)
        assert isinstance(updater._resolution_service, SyncResolutionService)
