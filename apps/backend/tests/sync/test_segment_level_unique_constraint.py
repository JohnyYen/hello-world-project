"""
Tests for SegmentLevel unique constraint and Pydantic schemas.

Tests verify:
- UniqueConstraint on (level_number_id, segment_number) enforces uniqueness
- SegmentLevelResponse includes segment_number: int
- SegmentLevelCreate.segment_number is Optional[int] and defaults to None
"""

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from src.game.domain.segment_level import SegmentLevel
from src.game.api.v1.schemas.segment_level import (
    SegmentLevelCreate,
    SegmentLevelResponse,
)


class TestSegmentLevelUniqueConstraint:
    """Tests for SegmentLevel unique constraint definition."""

    def test_unique_constraint_defined_on_model(self):
        constraints = SegmentLevel.__table_args__
        assert constraints is not None

        if isinstance(constraints, tuple):
            uq_constraints = [
                c for c in constraints if isinstance(c, UniqueConstraint)
            ]
        elif isinstance(constraints, UniqueConstraint):
            uq_constraints = [constraints]
        else:
            uq_constraints = []

        assert len(uq_constraints) >= 1

        uq = uq_constraints[0]
        col_names = {c.name for c in uq.columns}
        assert col_names == {"level_number_id", "segment_number"}

    def test_segment_level_column_definition(self):
        segment_number_col = SegmentLevel.__table__.c["segment_number"]
        assert segment_number_col.nullable is False


class TestSegmentLevelSchemas:
    """Tests for SegmentLevel Pydantic schemas."""

    def test_segment_level_response_has_segment_number(self):
        response = SegmentLevelResponse(
            id=str(uuid4()),
            level_id=1,
            segment_number=3,
            created_at=datetime.now(timezone.utc),
        )
        assert response.segment_number == 3

    def test_segment_level_create_segment_number_optional(self):
        create = SegmentLevelCreate()
        assert create.segment_number is None

    def test_segment_level_create_with_segment_number(self):
        create = SegmentLevelCreate(segment_number=5)
        assert create.segment_number == 5
