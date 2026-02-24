from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.xapi_statement_repository import (
    XAPIStatementRepository,
)
from src.statistic.domain.xapi_statement import XAPIStatement
from src.statistic.api.v1.schemas.xapi_statement import (
    XAPIStatementCreate,
    XAPIStatementResponse,
)


class XAPIStatementService:
    """
    Service for processing and storing xAPI statements.

    Handles parsing of xAPI statements, extraction of game-specific fields,
    and batch processing for high-volume ingestion.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Initialize the service with database session.

        Args:
            db: Async database session
        """
        self.db = db
        self.repository = XAPIStatementRepository(db)

    def _parse_statement(self, statement: XAPIStatementCreate) -> Dict[str, Any]:
        """
        Parse xAPI statement and extract fields for database storage.

        Args:
            statement: xAPI statement Pydantic model

        Returns:
            Dictionary with parsed fields for database storage
        """
        now = datetime.now(timezone.utc)

        # Generate UUID if not provided
        statement_id = statement.id or str(uuid4())

        # Parse actor
        actor_mbox = None
        actor_account_name = None
        actor_account_homepage = None

        if statement.actor.mbox:
            actor_mbox = statement.actor.mbox
        if statement.actor.account:
            actor_account_name = statement.actor.account.get("name")
            actor_account_homepage = statement.actor.account.get("homePage")

        # Parse verb
        verb_id = statement.verb.id
        verb_display = statement.verb.display

        # Parse object
        object_id = statement.object.id
        object_type = statement.object.object_type
        object_definition_type = None
        object_definition_name = None

        if statement.object.definition:
            object_definition_type = statement.object.definition.type
            object_definition_name = statement.object.definition.name

        # Parse context
        platform = None
        language = None
        context_extensions = None

        if statement.context:
            platform = statement.context.platform
            language = statement.context.language
            context_extensions = statement.context.extensions

        # Parse result
        result_score_raw = None
        result_score_min = None
        result_score_max = None
        result_score_scaled = None
        result_success = None
        result_completion = None
        result_duration = None
        result_response = None
        result_extensions = None

        if statement.result:
            if statement.result.score:
                result_score_raw = (
                    str(statement.result.score.raw)
                    if statement.result.score.raw is not None
                    else None
                )
                result_score_min = (
                    str(statement.result.score.min)
                    if statement.result.score.min is not None
                    else None
                )
                result_score_max = (
                    str(statement.result.score.max)
                    if statement.result.score.max is not None
                    else None
                )
                result_score_scaled = (
                    str(statement.result.score.scaled)
                    if statement.result.score.scaled is not None
                    else None
                )
            result_success = statement.result.success
            result_completion = statement.result.completion
            result_duration = statement.result.duration
            result_response = statement.result.response
            result_extensions = statement.result.extensions

        # Parse timestamps
        timestamp = statement.timestamp or now
        stored = statement.stored or now

        # Extract game-specific fields from object ID and extensions
        # Object ID format: hello-world://segment/level_1_seg_3
        student_id = None
        game_id = None
        level_id = None
        segment_id = None

        # Try to extract from actor account name (usually student_id)
        if actor_account_name:
            try:
                student_id = int(actor_account_name)
            except (ValueError, TypeError):
                pass

        # Try to extract from context extensions
        if context_extensions:
            # Extract game_id from extensions
            game_ext = context_extensions.get(
                "http://hello-world-game.com/extensions/game_id"
            )
            if game_ext:
                try:
                    game_id = int(game_ext)
                except (ValueError, TypeError):
                    pass

            # Extract level_id from extensions
            level_ext = context_extensions.get(
                "http://hello-world-game.com/extensions/level_id"
            )
            if level_ext:
                try:
                    level_id = int(level_ext)
                except (ValueError, TypeError):
                    pass

            # Extract segment_id from extensions
            segment_ext = context_extensions.get(
                "http://hello-world-game.com/extensions/segment_id"
            )
            if segment_ext:
                try:
                    segment_id = int(segment_ext)
                except (ValueError, TypeError):
                    pass

        # Also try to parse from object ID if it's in hello-world format
        # Format: hello-world://segment/level_X_seg_Y or hello-world://level/X
        if object_id.startswith("hello-world://"):
            parts = object_id.replace("hello-world://", "").split("/")
            if len(parts) >= 2:
                if parts[0] == "segment" and len(parts) >= 2:
                    # hello-world://segment/level_1_seg_3
                    segment_part = parts[1]
                    if "seg_" in segment_part:
                        try:
                            segment_id = int(segment_part.split("_")[-1])
                            # Also try to extract level from segment name
                            if "level_" in segment_part:
                                level_str = segment_part.split("_")[1]
                                level_id = int(level_str)
                        except (ValueError, IndexError):
                            pass
                elif parts[0] == "level" and len(parts) >= 2:
                    # hello-world://level/1
                    try:
                        level_id = int(parts[1])
                    except ValueError:
                        pass

        # Build the full statement JSON
        statement_json = statement.model_dump(mode="json")
        # Fix the alias for 'object' key
        if "object" in statement_json and statement.object:
            statement_json["object"] = statement.model_dump(mode="json").get("object")

        return {
            # Primary key (UUID)
            "id": statement_id,
            # Actor
            "actor_mbox": actor_mbox,
            "actor_account_name": actor_account_name,
            "actor_account_homepage": actor_account_homepage,
            # Verb
            "verb_id": verb_id,
            "verb_display": verb_display,
            # Object
            "object_id": object_id,
            "object_type": object_type,
            "object_definition_type": object_definition_type,
            "object_definition_name": object_definition_name,
            # Context
            "platform": platform,
            "language": language,
            "context_extensions": context_extensions,
            "context_platform": platform,
            # Result
            "result_score_raw": result_score_raw,
            "result_score_min": result_score_min,
            "result_score_max": result_score_max,
            "result_score_scaled": result_score_scaled,
            "result_success": result_success,
            "result_completion": result_completion,
            "result_duration": result_duration,
            "result_response": result_response,
            "result_extensions": result_extensions,
            # Timestamps
            "timestamp": timestamp,
            "stored": stored,
            # Full statement
            "statement": statement_json,
            # Game-specific
            "student_id": student_id,
            "game_id": game_id,
            "level_id": level_id,
            "segment_id": segment_id,
        }

    async def save_statement(self, statement: XAPIStatementCreate) -> XAPIStatement:
        """
        Save a single xAPI statement.

        Args:
            statement: xAPI statement to save

        Returns:
            Created XAPIStatement instance
        """
        parsed_data = self._parse_statement(statement)
        return await self.repository.create(parsed_data)

    async def save_batch(
        self, statements: List[XAPIStatementCreate]
    ) -> List[XAPIStatement]:
        """
        Save multiple xAPI statements (batch).

        Args:
            statements: List of xAPI statements to save

        Returns:
            List of created XAPIStatement instances
        """
        parsed_statements = [self._parse_statement(s) for s in statements]
        return await self.repository.create_batch(parsed_statements)

    async def get_statement(self, statement_id: str) -> Optional[XAPIStatement]:
        """
        Get a statement by its ID.

        Args:
            statement_id: Statement UUID

        Returns:
            XAPIStatement if found, None otherwise
        """
        return await self.repository.get_by_statement_id(statement_id)

    async def get_statements(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_student(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by student ID.

        Args:
            student_id: Student ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        return await self.repository.get_by_student_id(
            student_id=student_id,
            skip=skip,
            limit=limit,
        )

    async def get_by_verb(
        self,
        verb_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by verb ID.

        Args:
            verb_id: Verb ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        return await self.repository.get_by_verb(
            verb_id=verb_id,
            skip=skip,
            limit=limit,
        )

    async def get_by_game(
        self,
        game_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by game ID.

        Args:
            game_id: Game ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        return await self.repository.get_by_game_id(
            game_id=game_id,
            skip=skip,
            limit=limit,
        )

    async def get_by_level(
        self,
        level_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by level ID.

        Args:
            level_id: Level ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        return await self.repository.get_by_level_id(
            level_id=level_id,
            skip=skip,
            limit=limit,
        )
