from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, asc
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.statistic.domain.xapi_statement import XAPIStatement


class XAPIStatementRepository(BaseRepository[XAPIStatement]):
    """
    Repository for xAPI Statement storage and retrieval.

    Optimized for high-volume ingestion (10K+ statements/session) with
    efficient query methods for analytics.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, XAPIStatement)

    async def create(self, data: Dict[str, Any]) -> XAPIStatement:
        """
        Create a new xAPI statement.

        Args:
            data: Dictionary with statement data

        Returns:
            Created XAPIStatement instance
        """
        return await super().create(data)

    async def create_batch(
        self, statements_data: List[Dict[str, Any]]
    ) -> List[XAPIStatement]:
        """
        Create multiple xAPI statements efficiently (batch insert).

        Args:
            statements_data: List of statement dictionaries

        Returns:
            List of created XAPIStatement instances
        """
        created_statements = []
        for data in statements_data:
            stmt = await self.create(data)
            created_statements.append(stmt)
        return created_statements

    async def get_by_id(self, statement_id: int) -> Optional[XAPIStatement]:
        """
        Get statement by database ID.

        Args:
            statement_id: Database ID of the statement

        Returns:
            XAPIStatement if found, None otherwise
        """
        return await super().get_by_id(statement_id)

    async def get_by_statement_id(self, statement_uuid: str) -> Optional[XAPIStatement]:
        """
        Get statement by xAPI statement UUID.

        Args:
            statement_uuid: xAPI statement ID (UUID string)

        Returns:
            XAPIStatement if found, None otherwise
        """
        filters = {"id": statement_uuid}
        return await self.get_one_by_filters(filters)

    async def get_by_actor(
        self,
        actor_account_name: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by actor account name (student_id).

        Args:
            actor_account_name: Actor account name (usually student_id)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        filters = {"actor_account_name": actor_account_name}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_student_id(
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
        filters = {"student_id": student_id}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
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
            verb_id: Verb ID (e.g., 'http://adlnet.gov/expapi/verbs/completed')
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        filters = {"verb_id": verb_id}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_object(
        self,
        object_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements by object ID (activity).

        Args:
            object_id: Object/Activity ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        filters = {"object_id": object_id}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_game_id(
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
        filters = {"game_id": game_id}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_level_id(
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
        filters = {"level_id": level_id}
        return await self.get_by_filters(
            filters,
            skip=skip,
            limit=limit,
            order_by="timestamp",
            descending=True,
        )

    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[XAPIStatement]:
        """
        Get statements within a date range.

        Args:
            start_date: Start date
            end_date: End date
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of XAPIStatement instances
        """
        query = (
            select(XAPIStatement)
            .where(
                and_(
                    XAPIStatement.timestamp >= start_date,
                    XAPIStatement.timestamp <= end_date,
                )
            )
            .order_by(desc(XAPIStatement.timestamp))
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: str = "timestamp",
        descending: bool = True,
    ) -> List[XAPIStatement]:
        """
        Get all statements with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include deleted statements
            order_by: Field to order by
            descending: Order direction

        Returns:
            List of XAPIStatement instances
        """
        return await super().get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            order_by=order_by,
            descending=descending,
        )

    async def count_by_student(self, student_id: int) -> int:
        """
        Count statements for a student.

        Args:
            student_id: Student ID

        Returns:
            Total count of statements
        """
        filters = {"student_id": student_id}
        return await self.count(filters)

    async def count_by_verb(self, verb_id: str) -> int:
        """
        Count statements for a verb.

        Args:
            verb_id: Verb ID

        Returns:
            Total count of statements
        """
        filters = {"verb_id": verb_id}
        return await self.count(filters)
