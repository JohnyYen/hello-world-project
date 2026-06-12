"""
Mapper for xapi_statement sync events from the game client.

The game client builds xAPI statements and sends them as sync events
with event_type="xapi_statement". This mapper handles two input formats:

1. Complete xAPI statement (game format) - Full xAPI 1.0 structure
2. Legacy simplified payload (legacy format) - Flattened game format

Game payload structure (legacy):
{
    "statement_id": "<uuid>",
    "verb_id": "http://adlnet.gov/expapi/verbs/completed",
    "verb_display": "completó",
    "object_type": "level|game|assessment",
    "object_id": "<id string>",
    "object_name": "<display name>",
    "actor_id": "<user UUID>",
    "result": {
        "score_raw": <float>,
        "score_scaled": <float>,
        "success": <bool>,
        "completion": <bool>,
        "duration": "<ISO 8601 duration>"
    },
    "timestamp": "<ISO datetime>"
}

Complete xAPI statement structure (new):
{
    "id": "<uuid>",
    "actor": {"account": {"homePage": "hello-world-game", "name": "<user_id>"}},
    "verb": {"id": "<verb_iri>", "display": {"es": "<display_text>"}},
    "object": {"id": "<object_id>", "definition": {"type": "<activity_type>", "name": {"es": "<object_name>"}}},
    "result": {"success": <bool>, "completion": <bool>, "score": {"raw": <num>, "scaled": <num>}},
    "context": {"platform": "Hello World Game", "language": "es", "extensions": {}},
    "timestamp": "<iso_datetime>"
}
"""

import re
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Any

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


# Mapping from game object_type values to xAPI activity type IRIs
OBJECT_TYPE_TO_ACTIVITY_TYPE = {
    "level": XAPIActivityTypes.LEVEL,
    "game": XAPIActivityTypes.GAME,
    "assessment": XAPIActivityTypes.LESSON,
    "segment": XAPIActivityTypes.SEGMENT,
    "exercise": XAPIActivityTypes.EXERCISE,
    "puzzle": XAPIActivityTypes.PUZZLE,
}

# Default activity type for unknown object types
DEFAULT_ACTIVITY_TYPE = XAPIActivityTypes.ACTIVITY


class SyncEventToXAPIStatementMapper:
    """
    Maps sync events with event_type='xapi_statement' to XAPIStatementCreate.

    The game client already builds xAPI statements internally and sends them
    as sync events. This mapper converts the game's simplified format into
    the full XAPIStatementCreate expected by the xAPI storage layer.
    """

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
        sync_session_result = await self.db.execute(
            select(SyncEvent)
            .options(selectinload(SyncEvent.sync_session))
            .where(SyncEvent.id == event.id)
        )
        loaded_event = sync_session_result.scalar_one_or_none()

        if not loaded_event or not loaded_event.sync_session:
            return None

        instance_id = loaded_event.sync_session.instance_id

        from src.game.domain.game_instance import GameInstance

        instance_result = await self.db.execute(
            select(GameInstance).where(GameInstance.id == instance_id)
        )
        game_instance = instance_result.scalar_one_or_none()

        if not game_instance:
            return None

        return game_instance.student_id

    def _build_actor(self, student_id: int | None, payload: dict) -> XAPIActor:
        """
        Build XAPIActor from student_id or payload actor_id.

        Args:
            student_id: Student ID from relationship chain
            payload: Event payload with optional actor_id

        Returns:
            XAPIActor: The actor for the xAPI statement
        """
        actor_name = str(student_id) if student_id else payload.get("actor_id", "unknown")

        return XAPIActor(
            account={
                "homePage": "hello-world-game",
                "name": actor_name,
            }
        )

    def _build_verb(self, payload: dict) -> XAPIVerb:
        """
        Build XAPIVerb from payload verb_id and verb_display.

        Args:
            payload: Event payload with verb_id and verb_display

        Returns:
            XAPIVerb: The verb for the xAPI statement
        """
        verb_id = payload.get("verb_id", XAPIVerbs.EXPERIENCED)
        verb_display = payload.get("verb_display")

        display = None
        if verb_display:
            display = {"es": verb_display}

        return XAPIVerb(id=verb_id, display=display)

    def _build_activity_type(self, object_type: str | None) -> str:
        """
        Map game object_type to xAPI activity type IRI.

        Args:
            object_type: Game object type ('level', 'game', 'assessment', etc.)

        Returns:
            str: xAPI activity type IRI
        """
        if not object_type:
            return DEFAULT_ACTIVITY_TYPE

        object_type_lower = object_type.lower()
        return OBJECT_TYPE_TO_ACTIVITY_TYPE.get(object_type_lower, DEFAULT_ACTIVITY_TYPE)

    def _build_object(self, payload: dict) -> XAPIActivity:
        """
        Build XAPIActivity from payload object fields.

        The object_id from the game is a simple string (e.g., "1" for a level).
        We wrap it into the hello-world URI format.

        Args:
            payload: Event payload with object_id, object_type, object_name

        Returns:
            XAPIActivity: The activity object for the xAPI statement
        """
        object_id = payload.get("object_id", "unknown")
        object_type = payload.get("object_type")
        object_name = payload.get("object_name")

        activity_type = self._build_activity_type(object_type)

        # Build IRI for the object
        # The game may now send compound URIs (hello-world://level/{n}/segment/{m})
        # or plain object_ids (e.g., "1" for legacy). Detect and handle both.
        if object_type == "level":
            if re.match(r"^hello-world://level/\d+/segment/\d+$", object_id):
                iri = object_id  # Already a valid compound URI, use as-is
            else:
                iri = f"hello-world://level/{object_id}"
        elif object_type == "segment":
            iri = f"hello-world://segment/{object_id}"
        else:
            iri = f"hello-world://{object_type}/{object_id}" if object_type else f"hello-world://{object_id}"

        name = None
        if object_name:
            name = {"es": object_name}

        return XAPIActivity(
            id=iri,
            object_type="Activity",
            definition=XAPIActivityDefinition(
                type=activity_type,
                name=name,
            ),
        )

    def _build_result(self, payload: dict) -> XAPIResult | None:
        """
        Build XAPIResult from payload result fields.

        Args:
            payload: Event payload with optional result dict

        Returns:
            XAPIResult | None: The result or None if no result data
        """
        result_data = payload.get("result")
        if not result_data:
            return None

        score = None
        score_raw = result_data.get("score_raw")
        score_scaled = result_data.get("score_scaled")

        if score_raw is not None or score_scaled is not None:
            score = XAPIScore(
                raw=score_raw,
                scaled=score_scaled,
            )

        return XAPIResult(
            score=score,
            success=result_data.get("success"),
            completion=result_data.get("completion"),
            duration=result_data.get("duration"),
        )

    def _build_context(self, payload: dict) -> XAPIContext | None:
        """
        Build XAPIContext from payload.

        Args:
            payload: Event payload

        Returns:
            XAPIContext | None: The context or None
        """
        return XAPIContext(
            platform="Hello World Game",
            language="es",
        )

    async def map(self, event: SyncEvent) -> XAPIStatementCreate:
        """
        Map a SyncEvent with event_type='xapi_statement' to XAPIStatementCreate.

        This mapper handles two input formats:
        1. Complete xAPI statement (game format) - wrapped in sync event payload
        2. Simplified sync event payload (legacy format)

        Args:
            event: The sync event with xAPI statement data in payload

        Returns:
            XAPIStatementCreate: The mapped xAPI statement

        Raises:
            ValueError: If the event payload is empty or missing required fields
        """
        payload = event.payload or {}

        if not payload:
            raise ValueError("xapi_statement event has no payload")

        # Check if this is a complete xAPI statement (game format)
        # A complete xAPI statement will have fields like actor, verb, object, result at the top level
        if "actor" in payload and "verb" in payload and "object" in payload:
            # This is a complete xAPI statement - use it directly
            return self._map_complete_xapi_statement(payload)
        else:
            # This is the legacy simplified payload format
            return await self._map_legacy_payload(payload, event)

    def _map_complete_xapi_statement(self, statement_data: dict) -> XAPIStatementCreate:
        """
        Map a complete xAPI statement (game format) to XAPIStatementCreate.
        
        Args:
            statement_data: Complete xAPI statement data with actor, verb, object, result, etc.
            
        Returns:
            XAPIStatementCreate: The mapped xAPI statement
        """
        # Get student_id from relationship chain
        # The actor should contain the account with student_id
        actor_name = statement_data.get("actor", {}).get("account", {}).get("name", "")
        
        # Parse timestamp
        timestamp = statement_data.get("timestamp")
        if timestamp:
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except (ValueError, TypeError):
                # Use current time if timestamp is invalid
                timestamp = datetime.now(timezone.utc)
        else:
            timestamp = datetime.now(timezone.utc)

        return XAPIStatementCreate(
            id=statement_data.get("id", str(uuid4())),
            actor=XAPIActor(
                mbox=statement_data.get("actor", {}).get("mbox"),
                mbox_sha1sum=statement_data.get("actor", {}).get("mbox_sha1sum"),
                account={
                    "homePage": statement_data.get("actor", {}).get("account", {}).get("homePage", "hello-world-game"),
                    "name": actor_name
                },
                name=statement_data.get("actor", {}).get("name"),
                object_type=statement_data.get("actor", {}).get("object_type")
            ),
            verb=XAPIVerb(
                id=statement_data.get("verb", {}).get("id", XAPIVerbs.EXPERIENCED),
                display={"es": statement_data.get("verb", {}).get("display", {}).get("es", "")}
            ),
            object=XAPIActivity(
                id=statement_data.get("object", {}).get("id", ""),
                object_type=statement_data.get("object", {}).get("object_type", "Activity"),
                definition=XAPIActivityDefinition(
                    type=statement_data.get("object", {}).get("definition", {}).get("type", ""),
                    name=statement_data.get("object", {}).get("definition", {}).get("name", {}),
                    description=statement_data.get("object", {}).get("definition", {}).get("description"),
                    extensions=statement_data.get("object", {}).get("definition", {}).get("extensions")
                )
            ),
            result=XAPIResult(
                score=XAPIScore(
                    raw=statement_data.get("result", {}).get("score", {}).get("raw"),
                    scaled=statement_data.get("result", {}).get("score", {}).get("scaled"),
                    min=statement_data.get("result", {}).get("score", {}).get("min"),
                    max=statement_data.get("result", {}).get("score", {}).get("max")
                ) if statement_data.get("result", {}).get("score") else None,
                success=statement_data.get("result", {}).get("success"),
                completion=statement_data.get("result", {}).get("completion"),
                response=statement_data.get("result", {}).get("response"),
                duration=statement_data.get("result", {}).get("duration"),
                extensions=statement_data.get("result", {}).get("extensions")
            ) if statement_data.get("result") else None,
            context=XAPIContext(
                registration=statement_data.get("context", {}).get("registration"),
                platform=statement_data.get("context", {}).get("platform", "Hello World Game"),
                language=statement_data.get("context", {}).get("language", "es"),
                instructor=statement_data.get("context", {}).get("instructor"),
                team=statement_data.get("context", {}).get("team"),
                context_activities=statement_data.get("context", {}).get("context_activities"),
                extensions=statement_data.get("context", {}).get("extensions")
            ),
            timestamp=timestamp,
            stored=datetime.now(timezone.utc),
            authority=statement_data.get("authority"),
            version=statement_data.get("version"),
            attachments=statement_data.get("attachments")
        )

    async def _map_legacy_payload(self, payload: dict, event: SyncEvent) -> XAPIStatementCreate:
        """
        Map legacy simplified payload (backward compatibility).

        Args:
            payload: Legacy payload format with flattened fields
            event: The sync event

        Returns:
            XAPIStatementCreate: The mapped xAPI statement
        """
        # Get student_id from relationship chain, fallback to actor_id in payload
        student_id = await self._get_student_id(event)

        # Parse timestamp from payload or use event timestamp
        timestamp_str = payload.get("timestamp")
        timestamp = event.timestamp
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except (ValueError, TypeError):
                pass

        return XAPIStatementCreate(
            id=payload.get("statement_id") or str(uuid4()),
            actor=self._build_actor(student_id, payload),
            verb=self._build_verb(payload),
            object=self._build_object(payload),
            result=self._build_result(payload),
            context=self._build_context(payload),
            timestamp=timestamp,
            stored=datetime.now(timezone.utc),
        )
