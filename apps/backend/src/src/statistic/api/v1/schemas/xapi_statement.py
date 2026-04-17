from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, List, Dict
from enum import Enum


class XAPIActorType(str, Enum):
    """xAPI Actor types."""

    AGENT = "Agent"
    GROUP = "Group"


class XAPIActor(BaseModel):
    """xAPI Actor - Who performed the action."""

    mbox: Optional[str] = Field(None, description="Mailto URI of actor")
    mbox_sha1sum: Optional[str] = Field(None, description="SHA1 hash of actor email")
    account: Optional[Dict[str, str]] = Field(
        None, description="Account object with homePage and name"
    )
    name: Optional[str] = Field(None, description="Display name of actor")
    object_type: Optional[XAPIActorType] = Field(None, description="Agent or Group")


class XAPIVerbDisplay(BaseModel):
    """xAPI Verb display (localized)."""

    # This is a flexible model that accepts any locale code as key
    # e.g., {"en-US": "completed", "es": "completado"}
    pass


class XAPIVerb(BaseModel):
    """xAPI Verb - The action performed."""

    id: str = Field(..., description="IRI of the verb")
    display: Optional[Dict[str, str]] = Field(
        None, description="Human readable display of verb"
    )


class XAPIActivityDefinition(BaseModel):
    """xAPI Activity definition with type, name, description."""

    type: Optional[str] = Field(None, description="Activity type IRI")
    name: Optional[Dict[str, str]] = Field(
        None, description="Activity name (localized)"
    )
    description: Optional[Dict[str, str]] = Field(
        None, description="Activity description (localized)"
    )
    extensions: Optional[Dict[str, Any]] = Field(None, description="Custom extensions")


class XAPIActivity(BaseModel):
    """xAPI Activity - The object of the action."""

    id: str = Field(..., description="IRI of the activity")
    object_type: Optional[str] = Field(default="Activity", description="Type of object")
    definition: Optional[XAPIActivityDefinition] = Field(
        None, description="Activity definition"
    )


class XAPIScore(BaseModel):
    """xAPI Score - Quantitative result."""

    raw: Optional[float] = Field(None, description="Raw score")
    min: Optional[float] = Field(None, description="Minimum score")
    max: Optional[float] = Field(None, description="Maximum score")
    scaled: Optional[float] = Field(None, description="Scaled score (0-1)")


class XAPIResult(BaseModel):
    """xAPI Result - The result of the action (quantitative and qualitative)."""

    score: Optional[XAPIScore] = Field(None, description="Score object")
    success: Optional[bool] = Field(None, description="Success of the activity")
    completion: Optional[bool] = Field(None, description="Completion of the activity")
    response: Optional[str] = Field(None, description="Response/answer provided")
    duration: Optional[str] = Field(
        None, description="Duration in ISO 8601 format (PTnHnMnS)"
    )
    extensions: Optional[Dict[str, Any]] = Field(
        None, description="Custom result extensions"
    )


class XAPIContextRegistration(BaseModel):
    """xAPI Context registration."""

    name: Optional[str] = None
    description: Optional[Dict[str, str]] = None


class XAPIContext(BaseModel):
    """xAPI Context - Additional context information."""

    registration: Optional[str] = Field(None, description="Registration UUID")
    platform: Optional[str] = Field(
        None, description="Platform (e.g., 'Hello World Game')"
    )
    language: Optional[str] = Field(
        None, description="Language code (e.g., 'es', 'en')"
    )
    instructor: Optional[XAPIActor] = Field(None, description="Instructor")
    team: Optional[XAPIActor] = Field(None, description="Team/group")
    context_activities: Optional[Dict[str, Any]] = Field(
        None, description="Related activities"
    )
    extensions: Optional[Dict[str, Any]] = Field(
        None, description="Custom context extensions"
    )


class XAPIStatementCreate(BaseModel):
    """
    xAPI Statement schema for receiving statements from game client.
    Supports full xAPI 1.0 specification with game-specific context.
    """

    id: Optional[str] = Field(
        None, description="Statement ID (UUID), auto-generated if not provided"
    )
    actor: XAPIActor = Field(..., description="Who performed the action")
    verb: XAPIVerb = Field(..., description="The action performed")
    object: XAPIActivity = Field(
        ..., alias="object", description="The object of the action"
    )
    result: Optional[XAPIResult] = Field(
        None, description="Result of the action (quantitative)"
    )
    context: Optional[XAPIContext] = Field(
        None, description="Context (qualitative info)"
    )
    timestamp: Optional[datetime] = Field(
        None, description="When the statement occurred"
    )
    stored: Optional[datetime] = Field(
        None, description="When the statement was stored"
    )
    authority: Optional[XAPIActor] = Field(None, description="Who stored the statement")
    version: Optional[str] = Field(None, description="xAPI version (default: 1.0.3)")
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="Attachments")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "actor": {
                    "account": {"homePage": "hello-world-game", "name": "student_123"}
                },
                "verb": {"id": "http://adlnet.gov/expapi/verbs/completed"},
                "object": {
                    "id": "hello-world://segment/level_1_seg_3",
                    "definition": {
                        "type": "http://adlnet.gov/expapi/activities/lesson",
                        "name": {"es": "Segmento 3 - Variables"},
                    },
                },
                "result": {
                    "success": True,
                    "completion": True,
                    "score": {"raw": 85, "min": 0, "max": 100, "scaled": 0.85},
                    "duration": "PT5M30S",
                },
                "context": {
                    "platform": "Hello World Game v1.0",
                    "language": "es",
                    "extensions": {
                        "http://hello-world-game.com/extensions/game_session": "session_abc",
                        "http://hello-world-game.com/extensions/attempts": 2,
                        "http://hello-world-game.com/extensions/hints_used": 1,
                    },
                },
                "timestamp": "2026-02-13T10:30:00Z",
            }
        }


class XAPIStatementBatchCreate(BaseModel):
    """Batch of xAPI statements."""

    statements: List[XAPIStatementCreate] = Field(..., min_length=1, max_length=1000)


class XAPIStatementResponse(BaseModel):
    """xAPI Statement response after storage."""

    id: str
    actor: XAPIActor
    verb: XAPIVerb
    object: XAPIActivity
    result: Optional[XAPIResult] = None
    context: Optional[XAPIContext] = None
    timestamp: datetime
    stored: datetime

    class Config:
        from_attributes = True


class XAPIStatementListResponse(BaseModel):
    """List of xAPI statements with pagination."""

    statements: List[XAPIStatementResponse]
    total: int
    skip: int
    limit: int


# Standard xAPI Verbs for games (extensible)
class XAPIVerbs:
    """Predefined xAPI verbs for game events."""

    INITIALIZED = "http://adlnet.gov/expapi/verbs/initialized"
    PROGRESSED = "http://adlnet.gov/expapi/verbs/progressed"
    ATTEMPTED = "http://adlnet.gov/expapi/verbs/attempted"
    COMPLETED = "http://adlnet.gov/expapi/verbs/completed"
    PASSED = "http://adlnet.gov/expapi/verbs/passed"
    FAILED = "http://adlnet.gov/expapi/verbs/failed"
    EXPERIENCED = "http://adlnet.gov/expapi/verbs/experienced"
    INTERACTED = "http://adlnet.gov/expapi/verbs/interacted"
    TERMINATED = "http://adlnet.gov/expapi/verbs/terminated"
    SUSPENDED = "http://adlnet.gov/expapi/verbs/suspended"
    RESUMED = "http://adlnet.gov/expapi/verbs/resumed"
    ANSWERED = "http://adlnet.gov/expapi/verbs/answered"
    LAUNCHED = "http://adlnet.gov/expapi/verbs/launched"
    WAITED = "http://adlnet.gov/expapi/verbs/waited"


# Standard xAPI Activity Types for games
class XAPIActivityTypes:
    """Predefined xAPI activity types for games."""

    COURSE = "http://adlnet.gov/expapi/activities/course"
    LESSON = "http://adlnet.gov/expapi/activities/lesson"
    MODULE = "http://adlnet.gov/expapi/activities/module"
    ACTIVITY = "http://adlnet.gov/expapi/activities/activity"
    GAME = "http://adlnet.gov/expapi/activities/game"
    LEVEL = "hello-world://activity/level"
    SEGMENT = "hello-world://activity/segment"
    EXERCISE = "hello-world://activity/exercise"
    PUZZLE = "hello-world://activity/puzzle"
