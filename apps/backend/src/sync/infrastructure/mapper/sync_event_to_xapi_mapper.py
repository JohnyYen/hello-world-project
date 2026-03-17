from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.sync.domain.sync_event import SyncEvent
from src.statistic.api.v1.schemas.xapi_statement import (
    XAPIStatementCreate,
    XAPIActor,
    XAPIVerb,
    XAPIActivity,
    XAPIActivityDefinition,
    XAPIResult,
    XAPIScore,
    XAPIContext,
    XAPIVerbs,
    XAPIActivityTypes,
)


class SyncEventToXAPIMapper:
    """
    Maps SyncEvent to xAPI Statement format.

    Transforms sync events from the game client into xAPI statements
    that can be stored and analyzed.
    """

    EVENT_TYPE_TO_VERB = {
        "error": XAPIVerbs.FAILED,
        "interaction": XAPIVerbs.INTERACTED,
        "hint_used": XAPIVerbs.PROGRESSED,
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_student_id(self, event: SyncEvent) -> int | None:
        """
        Get student_id by traversing the relationship chain:
        event -> sync_session -> game_instance -> student

        Args:
            event: The sync event

        Returns:
            int | None: The student ID if found
        """
        # First get the sync_session to find instance_id
        sync_session_result = await self.db.execute(
            select(SyncEvent)
            .options(selectinload(SyncEvent.sync_session))
            .where(SyncEvent.id == event.id)
        )
        loaded_event = sync_session_result.scalar_one_or_none()

        if not loaded_event or not loaded_event.sync_session:
            return None

        # Get the instance_id from sync_session
        instance_id = loaded_event.sync_session.instance_id

        # Now get the game_instance to find student_id
        from src.game.domain.game_instance import GameInstance

        instance_result = await self.db.execute(
            select(GameInstance).where(GameInstance.id == instance_id)
        )
        game_instance = instance_result.scalar_one_or_none()

        if not game_instance:
            return None

        return game_instance.student_id

    async def map(self, event: SyncEvent) -> XAPIStatementCreate:
        """
        Map a SyncEvent to an xAPIStatementCreate.

        Args:
            event: The sync event to map

        Returns:
            XAPIStatementCreate: The mapped xAPI statement
        """
        payload = event.payload or {}

        student_id = await self._get_student_id(event)
        if student_id is None:
            student_id = payload.get("student_id")
        level_id = payload.get("level_id")
        segment_id = payload.get("segment_id")
        game_id = payload.get("game_id")

        actor = XAPIActor(
            account={
                "homePage": "hello-world-game",
                "name": str(student_id) if student_id else "unknown",
            }
        )

        verb_id = self.EVENT_TYPE_TO_VERB.get(event.event_type, XAPIVerbs.EXPERIENCED)
        verb = XAPIVerb(id=verb_id, display={"en-US": event.event_type})

        object_id = self._build_object_id(level_id, segment_id)
        object_activity = XAPIActivity(
            id=object_id,
            object_type="Activity",
            definition=XAPIActivityDefinition(
                type=XAPIActivityTypes.SEGMENT,
                name={"en-US": f"Segment {segment_id}" if segment_id else "Unknown"},
            ),
        )

        result = self._build_result(event)

        extensions = {}
        if game_id:
            extensions["http://hello-world-game.com/extensions/game_id"] = game_id
        if level_id:
            extensions["http://hello-world-game.com/extensions/level_id"] = level_id
        if segment_id:
            extensions["http://hello-world-game.com/extensions/segment_id"] = segment_id

        context = XAPIContext(
            platform="Hello World Game",
            language="es",
            extensions=extensions if extensions else None,
        )

        return XAPIStatementCreate(
            id=str(uuid4()),
            actor=actor,
            verb=verb,
            object=object_activity,
            result=result,
            context=context,
            timestamp=event.timestamp,
            stored=datetime.now(timezone.utc),
        )

    def _build_object_id(self, level_id: int | None, segment_id: int | None) -> str:
        """
        Build the xAPI object ID from level and segment IDs.

        Args:
            level_id: The level ID
            segment_id: The segment ID

        Returns:
            str: The xAPI object ID
        """
        if level_id and segment_id:
            return f"hello-world://segment/level_{level_id}_seg_{segment_id}"
        elif level_id:
            return f"hello-world://level/{level_id}"
        else:
            return "hello-world://unknown"

    def _build_result(self, event: SyncEvent) -> XAPIResult | None:
        """
        Build the xAPI result from the event payload.

        Args:
            event: The sync event

        Returns:
            XAPIResult | None: The built result or None
        """
        payload = event.payload or {}

        if event.event_type == "error":
            return XAPIResult(
                success=False,
                response=payload.get("error_message", "Unknown error"),
            )

        if event.event_type == "hint_used":
            return XAPIResult(
                completion=False,
                extensions={"hints_used": payload.get("hints_count", 1)},
            )

        if event.event_type == "interaction":
            return XAPIResult(
                response=payload.get("interaction_type", "unknown"),
                completion=False,
            )

        return None
