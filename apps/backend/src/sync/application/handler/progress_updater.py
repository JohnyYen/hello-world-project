import logging
import math
import re
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.domain.sync_event import SyncEvent
from src.sync.domain.service.sync_resolution_service import SyncResolutionService
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress
from src.users.infrastructure.student_activity_log_repository import (
    StudentActivityLogRepository,
)
from src.users.domain.student import Student


logger = logging.getLogger(__name__)


class ProgressUpdater:
    """
    Updates Progress records based on sync event types.

    Handles the logic for updating different progress metrics
    based on the event type. For xapi_statement events, student_id
    and segment_level_id are resolved from the payload and sync
    session chain rather than expected directly in the payload.
    """

    def __init__(
        self,
        db: AsyncSession,
        resolution_service: Optional[SyncResolutionService] = None,
        activity_log_repo: Optional[StudentActivityLogRepository] = None,
    ):
        """
        Initialize the progress updater.

        Args:
            db: AsyncSession for database operations
            resolution_service: Optional SyncResolutionService for entity resolution chain.
                If not provided, a default instance is created.
            activity_log_repo: Optional StudentActivityLogRepository for logging student
                activity. If not provided, a default instance is created.
        """
        self.db = db
        self.repository = ProgressRepository(db)
        self._resolution_service = resolution_service or SyncResolutionService(db)
        self._activity_log_repo = activity_log_repo or StudentActivityLogRepository(db)

    async def update(self, event: SyncEvent) -> None:
        """
        Update progress based on the event type.

        Args:
            event: The sync event to process
        """
        payload = event.payload or {}

        # Resolve student_id from the sync session chain (most reliable).
        # The game sends actor_id=user_id in the payload, but progresses
        # FK references students.id — the chain resolves the correct one
        # (students.id ≠ user_id, they're different UUIDs).
        # The chain traversal: SyncSession -> GameInstance -> student_id (correct FK).
        student_id = payload.get("student_id")
        if not student_id:
            student_id = await self._resolve_student_id(event)

        # Resolve segment_level_id from payload or via sync session chain
        segment_level_id = payload.get("segment_level_id")
        if not segment_level_id:
            segment_level_id = await self._resolve_segment_level_id(event)

        if not student_id or not segment_level_id:
            logger.warning(
                f"Missing student_id or segment_level_id in event {event.id}"
            )
            return

        progress = await self.repository.get_by_student_and_segment(
            student_id=student_id,
            segment_level_id=segment_level_id,
        )

        if not progress:
            logger.info(
                f"Creating new progress record for student {student_id}, segment_level {segment_level_id}"
            )
            # Try to create, handle duplicate exception
            try:
                progress = await self._create_progress(student_id, segment_level_id)
            except Exception as e:
                # If creation fails due to duplicate, try to get existing one
                logger.warning(
                    f"Failed to create progress, trying to get existing: {str(e)}"
                )
                progress = await self.repository.get_by_student_and_segment(
                    student_id=student_id,
                    segment_level_id=segment_level_id,
                )
                if not progress:
                    logger.error(
                        f"Could not find or create progress for student {student_id}, segment_level {segment_level_id}"
                    )
                    return

        update_data = self._build_update_data(event)
        if update_data:
            await self.repository.update(progress.id, update_data)
            await self.db.commit()
            logger.info(f"Updated progress {progress.id} for event {event.id}")

        # Write to student_activity_log for xapi_statement events (heatmap data)
        if event.event_type == "xapi_statement" and student_id:
            await self._log_activity(event, student_id)



    def _build_update_data(self, event: SyncEvent) -> dict[str, Any]:
        """
        Build update data based on event type.

        Args:
            event: The sync event

        Returns:
            dict: The update data
        """
        payload = event.payload or {}
        update_data = {}

        event_type = event.event_type

        if event_type == "attempt":
            update_data["attempt_count"] = payload.get("count", 1)

        elif event_type == "error":
            current_errors = payload.get("count", 1)
            update_data["error_count"] = current_errors
            update_data["errors_details"] = payload.get("details")

        elif event_type == "hint_used":
            hints_count = payload.get("count", 1)
            update_data["hints_used_count"] = hints_count

        elif event_type == "score":
            update_data["efficiency_rating"] = payload.get("rating", 0)

        elif event_type == "level_completed":
            update_data["objectives_completed"] = payload.get("count", 1)

        elif event_type == "xapi_statement":
            # Extract progress data from xAPI statement payload
            # Handle both complete xAPI statement format and legacy format
            xapi_payload = payload

            # Detect if this is a complete xAPI statement (game format)
            # A complete xAPI statement has actor, verb, object, result at the top level
            is_complete_xapi = (
                "actor" in xapi_payload
                and "verb" in xapi_payload
                and "object" in xapi_payload
            )

            if is_complete_xapi:
                # Complete xAPI statement format (game sends standard xAPI 1.0)
                result = xapi_payload.get("result", {})
                verb_id = xapi_payload.get("verb", {}).get("id", "")
            else:
                # Legacy format - flattened fields
                result = payload.get("result", {})
                verb_id = payload.get("verb_id", "")

            # Level completed: update based on result
            # NOTE: "attempted" events MUST NOT set objectives_completed OR attempt_count.
            # The game sends attempted when a level starts (before any result),
            # and the builder defaults result_completion=true, which would
            # incorrectly mark the level as completed.
            if "attempted" not in verb_id:
                if "completed" in verb_id or result.get("completion") or result.get("success"):
                    update_data["objectives_completed"] = 1

                    # Set attempt_count from duration (ISO 8601) or default to 1.
                    # The game sends result.duration as PT{M}M{S}S which we parse as
                    # minutes. If no duration field is present, default to 1 attempt.
                    duration_str = result.get("duration") if result else None
                    duration_minutes = self._parse_duration_to_minutes(duration_str)
                    if duration_minutes is not None:
                        update_data["attempt_count"] = duration_minutes
                    else:
                        # No duration or empty duration — count as 1 attempt
                        update_data["attempt_count"] = 1

            # Map score to efficiency_rating (0-100 scale) - anytime score is present
            # Handle both standard xAPI format (result.score.scaled/raw) and legacy format (result.score_scaled/raw)
            # IMPORTANT: Always use explicit `is not None` checks, NEVER `or` for score
            # aggregation. `0.0` is a VALID score (student got 0%), but `or` treats it as
            # falsy and would fall through to the other field, producing wrong results.
            score = None
            if is_complete_xapi:
                # Standard xAPI 1.0 format: result.score.scaled or result.score.raw
                score_obj = result.get("score") if result else None
                if score_obj:
                    scaled = score_obj.get("scaled")
                    raw = score_obj.get("raw")
                    score = scaled if scaled is not None else raw
            else:
                # Legacy format: result has score_raw/score_scaled nested (game format)
                # The game sends result.score_raw and result.score_scaled (nested in result)
                if result:
                    score_raw = result.get("score_raw")
                    score_scaled = result.get("score_scaled")
                    score = score_scaled if score_scaled is not None else score_raw

            if score is not None:
                if isinstance(score, float) and score <= 1.0:
                    update_data["efficiency_rating"] = int(score * 100)
                else:
                    update_data["efficiency_rating"] = int(score)

        elif event_type == "raw_stats":
            # Bulk stats update - includes all metrics in one event
            update_data["attempt_count"] = payload.get("attempt_count", 0)
            update_data["error_count"] = payload.get("error_count", 0)
            update_data["hints_used_count"] = payload.get("hints_used_count", 0)
            update_data["errors_details"] = payload.get("errors_details")
            update_data["efficiency_rating"] = int(payload.get("efficiency_rating") or 0)
            update_data["objectives_completed"] = payload.get("objectives_completed", 0)

        elif event_type == "level_time":
            pass

        elif event_type == "difficulty_changed":
            pass

        elif event_type == "adaptation":
            pass

        return update_data

    @staticmethod
    def _parse_duration_to_minutes(duration: Optional[str]) -> Optional[int]:
        """
        Parse an ISO 8601 duration string to integer minutes (ceil).

        Supports PT{H}H{M}M{S}S format used by the game:
        - PT5M30S -> 6 (ceil 5.5)
        - PT30S -> 1 (ceil 0.5)
        - PT1H -> 60
        - PT1H30M -> 90
        - PT0S -> 0

        Args:
            duration: ISO 8601 duration string (e.g., "PT5M30S")

        Returns:
            Integer minutes (ceil), or None if invalid/missing
        """
        if not duration:
            return None

        # Match PT{H}H{M}M{S}S — all components are optional but at least one must match
        match = re.match(
            r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", duration.strip()
        )
        if not match:
            logger.warning(f"Could not parse duration string: '{duration}'")
            return None

        hours_str, minutes_str, seconds_str = match.groups()
        hours = int(hours_str) if hours_str else 0
        minutes = int(minutes_str) if minutes_str else 0
        seconds = int(seconds_str) if seconds_str else 0

        total_minutes = hours * 60 + minutes + seconds / 60.0
        return int(math.ceil(total_minutes))

    async def _resolve_user_id(self, student_id: UUID) -> Optional[UUID]:
        """
        Bridge from students.id to users.id for activity logging.

        StudentActivityLog.student_id FK references users.id, but the
        ProgressUpdater resolves students.id. This method bridges the gap.

        Args:
            student_id: The students.id value

        Returns:
            UUID of the User, or None if not found
        """
        query = select(Student.user_id).where(Student.id == student_id)
        result = await self.db.execute(query)
        user_id = result.scalar_one_or_none()
        if not user_id:
            logger.warning(
                f"Could not resolve user_id for student {student_id}"
            )
        return user_id

    async def _log_activity(
        self, event: SyncEvent, student_id: UUID
    ) -> None:
        """
        Log a student activity entry for xapi_statement events.

        Used to populate the student_activity_log table for heatmap
        and activity tracking in the dashboard.

        Args:
            event: The sync event being processed
            student_id: The resolved students.id
        """
        try:
            user_id = await self._resolve_user_id(student_id)
            if not user_id:
                return

            payload = event.payload or {}
            verb_id = ""
            object_id = ""
            duration_str = None

            # Extract fields from either complete xAPI or legacy format
            if "actor" in payload and "verb" in payload and "object" in payload:
                # Complete xAPI statement format
                verb_id = payload.get("verb", {}).get("id", "")
                object_id = payload.get("object", {}).get("id", "")
                result = payload.get("result", {})
                duration_str = result.get("duration") if result else None
            else:
                # Legacy format
                verb_id = payload.get("verb_id", "")
                object_id = payload.get("object_id", "")
                result = payload.get("result", {})
                duration_str = result.get("duration") if result else None

            metadata = {
                "verb_id": verb_id,
                "object_id": object_id,
                "duration": duration_str,
                "event_id": str(event.id),
            }

            await self._activity_log_repo.create_log(
                student_id=user_id,
                activity_type="xapi_statement",
                metadata=metadata,
            )
        except Exception as e:
            # Activity logging must NEVER break the sync pipeline
            logger.warning(
                f"Failed to log activity for event {event.id}: {str(e)}"
            )

    async def _resolve_student_id(self, event: SyncEvent) -> Optional[UUID]:
        """
        Resolve student_id from the sync session chain via SyncResolutionService.

        Traverses: SyncEvent → SyncSession → GameInstance → student_id

        Args:
            event: The sync event to resolve student_id for

        Returns:
            UUID of the Student, or None if it cannot be resolved
        """
        return await self._resolution_service.resolve_student_id(event.sync_session_id)

    async def _resolve_segment_level_id(self, event: SyncEvent) -> Optional[UUID]:
        """
        Resolve segment_level_id from payload or sync session chain.

        Two resolution paths:
          Path 1: xapi_statement events with object_type/object_id
          Path 2: raw_stats events with segment_id (int)

        Both delegate to SyncResolutionService for the chain traversal:
          SyncEvent → SyncSession → GameInstance → Level → SegmentLevel

        Args:
            event: The sync event to resolve segment_level_id for

        Returns:
            UUID of the SegmentLevel, or None if it cannot be resolved
        """
        payload = event.payload or {}

        # Handle both complete xAPI statement format and legacy format
        # Check if this is a complete xAPI statement (game format)
        xapi_payload = payload
        if "actor" in xapi_payload and "verb" in xapi_payload and "object" in xapi_payload:
            # Complete xAPI statement format - extract object_id from object.id
            object_data = xapi_payload.get("object", {})
            object_id = object_data.get("id", "")
        else:
            # Legacy format - flattened fields
            object_id = payload.get("object_id")

        # Path 1: xapi_statement with object_type/object_id
        if object_id:
            # Resolve (level_number, segment_number) from object_id
            resolved = self._resolve_level_and_segment_from_object_id(object_id)
            if resolved is not None:
                level_number, segment_number = resolved
                if segment_number is not None:
                    return await self._resolution_service.resolve_segment_level_id_from_object(
                        event.sync_session_id, level_number, segment_number
                    )
                # Legacy format — no segment_number available
                logger.warning(
                    f"Legacy xAPI object_id format without segment_number: "
                    f"'{object_id}'. Falling back to .limit(1) resolution."
                )
                return await self._resolution_service.resolve_segment_level_id_from_object(
                    event.sync_session_id, level_number
                )

        # Path 2: raw_stats with segment_id (maps to Level.level_number)
        segment_id = payload.get("segment_id")
        if segment_id is not None:
            try:
                level_number = int(segment_id)
            except (ValueError, TypeError):
                logger.warning(
                    f"Cannot parse segment_id '{segment_id}' as level number in event {event.id}"
                )
                return None
            return await self._resolution_service.resolve_segment_level_id_from_segment(
                event.sync_session_id, level_number
            )

        return None

    def _resolve_level_and_segment_from_object_id(
        self, object_id: str
    ) -> Optional[tuple[int, Optional[int]]]:
        """
        Resolve (level_number, segment_number) from xAPI object_id.

        Handles (in order):
        1. hello-world://level/{n}/segment/{m} -> (n, m) [new compound format]
        2. Plain integer strings (e.g., "5") -> (5, None) [legacy]
        3. hello-world://level/{n} -> (n, None) [legacy]
        4. hello-world://segment/level_{n}_seg_{m} -> (n, None) [legacy]
        5. hello-world://activity/course_{n} -> (n, None) [legacy]
        6. Invalid/empty -> None

        Args:
            object_id: xAPI object ID

        Returns:
            Tuple of (level_number, segment_number) or None if cannot extract
        """
        if not object_id:
            return None

        # 1. New compound format: hello-world://level/{n}/segment/{m}
        level_seg_match = re.match(
            r"^hello-world://level/(\d+)/segment/(\d+)$", object_id
        )
        if level_seg_match:
            return (int(level_seg_match.group(1)), int(level_seg_match.group(2)))

        # 2. Handle plain integer strings (legacy format)
        try:
            return (int(object_id), None)
        except (ValueError, TypeError):
            pass

        # 3. Handle hello-world://level/{n} format
        if object_id.startswith("hello-world://level/"):
            try:
                return (int(object_id.replace("hello-world://level/", "")), None)
            except (ValueError, TypeError):
                return None
        
        # 4. Handle hello-world://segment/level_{n}_seg_{m} format
        if object_id.startswith("hello-world://segment/"):
            try:
                segment_part = object_id.replace("hello-world://segment/", "")
                if "level_" in segment_part and "seg_" in segment_part:
                    level_part = segment_part.split("_")[1]  # "1_seg_3"
                    level_number = int(level_part.split("_")[0])  # "1"
                    return (level_number, None)
            except (ValueError, IndexError, TypeError):
                pass
        
        # 5. Handle hello-world://activity/course_{n} format
        if object_id.startswith("hello-world://activity/"):
            try:
                activity_part = object_id.replace("hello-world://activity/", "")
                if "_" in activity_part:
                    level_number = int(activity_part.split("_")[1])  # "course_1" -> 1
                    return (level_number, None)
            except (ValueError, IndexError, TypeError):
                pass
        
        return None

    async def _create_progress(
        self, student_id: UUID, segment_level_id: UUID
    ) -> Progress:
        """
        Create a new progress record.

        Args:
            student_id: The student UUID
            segment_level_id: The segment level UUID

        Returns:
            Progress: The created progress record
        """
        data = {
            "student_id": student_id,
            "segment_level_id": segment_level_id,
            "attempt_count": 0,
            "error_count": 0,
            "hints_used_count": 0,
            "errors_details": None,
            "objectives_completed": 0,
            "efficiency_rating": 0,
        }
        return await self.repository.create(data)
