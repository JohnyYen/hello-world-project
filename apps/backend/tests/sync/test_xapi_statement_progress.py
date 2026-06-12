"""
Integration test to verify xAPI statement progress update flow.

This test simulates the exact payload from the game to identify why
xAPI statements are not being converted to progress data.
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from src.sync.application.handler.progress_updater import ProgressUpdater
from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.service.sync_resolution_service import SyncResolutionService
from src.statistic.domain.progress import Progress


class TestXAPIStatementProgressIntegration:
    """Test that complete xAPI statements from the game create progress updates."""

    @pytest.mark.asyncio
    async def test_complete_xapi_statement_creates_progress_update(self):
        """
        Test that a complete xAPI statement (game format) creates progress.
        
        This is the EXACT statement format from the game:
        {
            "id": "0787d922-d59a-c77f-04fd-dc89db35cf21",
            "actor": {
                "account": {"homePage": "hello-world-game", "name": "9320b6e6-c37c-4186-869e-4bb548cfd83d"}
            },
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"es": "completó"}},
            "object": {
                "id": "hello-world://level/2",
                "definition": {"type": "hello-world://activity/level", "name": {"es": "Level 2"}}
            },
            "result": {"success": True, "completion": True},
            "context": {"platform": "Hello World Game", "language": "es"}
        }
        """
        # Setup mock services
        student_id = uuid4()
        segment_level_id = uuid4()
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
        mock_progress.attempt_count = 0
        mock_progress.efficiency_rating = 0
        mock_progress.objectives_completed = 0
        mock_repo.get_by_student_and_segment = AsyncMock(return_value=mock_progress)
        mock_repo.update = AsyncMock()
        
        updater = ProgressUpdater(mock_db, resolution_service=mock_svc)
        updater.repository = mock_repo
        
        # Create the exact xAPI statement from the game
        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "id": "0787d922-d59a-c77f-04fd-dc89db35cf21",
            "actor": {
                "mbox": None,
                "mbox_sha1sum": None,
                "account": {"homePage": "hello-world-game", "name": "9320b6e6-c37c-4186-869e-4bb548cfd83d"},
                "name": None,
                "object_type": None
            },
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"es": "completó"}},
            "object": {
                "id": "hello-world://level/2",
                "object_type": "Activity",
                "definition": {"type": "hello-world://activity/level", "name": {"es": "Level 2"}}
            },
            "result": {"score": None, "success": True, "completion": True, "response": None, "duration": "", "extensions": None},
            "context": {"platform": "Hello World Game", "language": "es"},
            "timestamp": "2026-06-11T13:55:21",
            "stored": "2026-06-11T17:55:22.089050Z",
        }
        event.timestamp = datetime.now(timezone.utc)
        
        await updater.update(event)
        
        # Verify resolution was called
        mock_svc.resolve_student_id.assert_called_once_with(sync_session_id)
        mock_svc.resolve_segment_level_id_from_object.assert_called_once_with(
            sync_session_id, 2  # Level 2 extracted from hello-world://level/2
        )
        
        # Verify progress was updated
        mock_repo.update.assert_called_once()
        call_args = mock_repo.update.call_args
        update_data = call_args[0][1]
        
        print(f"\nUpdate data: {update_data}")
        
        # Based on the xAPI statement:
        # - verb = completed, success = true, completion = true -> objectives_completed should be 1
        assert update_data.get("objectives_completed") == 1, \
            f"Expected objectives_completed=1, got {update_data.get('objectives_completed')}"
    
    @pytest.mark.asyncio
    async def test_xapi_statement_with_score_creates_efficiency_rating(self):
        """
        Test that a complete xAPI statement with score updates efficiency_rating.
        """
        student_id = uuid4()
        segment_level_id = uuid4()
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
        
        # xAPI statement with score (standard xAPI format)
        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "id": "test-statement-123",
            "actor": {
                "account": {"homePage": "hello-world-game", "name": "student-123"}
            },
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"es": "completó"}},
            "object": {
                "id": "hello-world://level/3",
                "definition": {"type": "hello-world://activity/level", "name": {"es": "Level 3"}}
            },
            "result": {
                "success": True,
                "completion": True,
                "score": {"raw": 85, "scaled": 0.85, "min": 0, "max": 100}  # Standard xAPI format
            },
        }
        event.timestamp = datetime.now(timezone.utc)
        
        await updater.update(event)
        
        # Verify progress was updated
        mock_repo.update.assert_called_once()
        call_args = mock_repo.update.call_args
        update_data = call_args[0][1]
        
        print(f"\nUpdate data with score: {update_data}")
        
        # Based on the xAPI statement:
        # - completion=true -> objectives_completed should be 1
        # - score.scaled=0.85 -> efficiency_rating should be 85
        assert update_data.get("objectives_completed") == 1, \
            f"Expected objectives_completed=1, got {update_data.get('objectives_completed')}"

        assert update_data.get("efficiency_rating") == 85, \
            f"Expected efficiency_rating=85 (from score.scaled=0.85), got {update_data.get('efficiency_rating')}"

    @pytest.mark.asyncio
    async def test_xapi_statement_with_raw_score(self):
        """
        Test that a complete xAPI statement with score.raw updates efficiency_rating.
        """
        student_id = uuid4()
        segment_level_id = uuid4()
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

        # xAPI statement with raw score (not scaled)
        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "actor": {"account": {"homePage": "hello-world-game", "name": "student-123"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"es": "completó"}},
            "object": {"id": "hello-world://level/1", "definition": {"type": "hello-world://activity/level"}},
            "result": {
                "success": True,
                "completion": True,
                "score": {"raw": 92, "min": 0, "max": 100}  # Raw score on 0-100 scale
            },
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        call_args = mock_repo.update.call_args
        update_data = call_args[0][1]

        # Raw score 92 should map directly to efficiency_rating 92
        assert update_data.get("efficiency_rating") == 92

    @pytest.mark.asyncio
    async def test_xapi_legacy_format_still_works(self):
        """
        Test backward compatibility: legacy flattened format still works.
        """
        student_id = uuid4()
        segment_level_id = uuid4()
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

        # Legacy format with flattened score fields - matches actual game _build_payload format
        event = MagicMock(spec=SyncEvent)
        event.id = 1
        event.event_type = "xapi_statement"
        event.sync_session_id = sync_session_id
        event.payload = {
            "object_type": "level",
            "object_id": "5",
            "verb_id": "http://adlnet.gov/expapi/verbs/completed",
            "result": {
                "score_raw": 75,  # Legacy format - game sends result.score_raw (nested)
                "score_scaled": 0.75,  # Legacy format - game sends result.score_scaled (nested)
                "completion": True,
            },
        }
        event.timestamp = datetime.now(timezone.utc)

        await updater.update(event)

        call_args = mock_repo.update.call_args
        update_data = call_args[0][1]

        # Legacy format score_raw should still work
        assert update_data.get("objectives_completed") == 1
        # Note: legacy format uses score_raw directly (75), not scaled
        assert update_data.get("efficiency_rating") == 75


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])