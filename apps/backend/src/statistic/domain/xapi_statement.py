from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    JSON,
    Text,
    Index,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class XAPIStatement(Base):
    """
    xAPI Statement storage model.

    Stores xAPI statements from game client with parsed fields for efficient querying.
    Supports full xAPI 1.0 specification while providing custom extensions for game context.
    """

    __tablename__ = "xapi_statements"

    # Primary key - UUID string as per xAPI specification
    id = Column(String(36), primary_key=True)

    # Parsed fields for efficient queries
    actor_mbox = Column(String(255), nullable=True, index=True)
    actor_account_name = Column(String(255), nullable=True, index=True)
    actor_account_homepage = Column(String(255), nullable=True)

    verb_id = Column(String(500), nullable=False, index=True)
    verb_display = Column(JSON, nullable=True)

    object_id = Column(String(1000), nullable=False, index=True)
    object_type = Column(String(100), nullable=True)
    object_definition_type = Column(String(255), nullable=True)
    object_definition_name = Column(JSON, nullable=True)

    # Context fields
    platform = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True)
    context_extensions = Column(JSON, nullable=True)
    context_platform = Column(String(255), nullable=True)

    # Result fields
    result_score_raw = Column(String(50), nullable=True)
    result_score_min = Column(String(50), nullable=True)
    result_score_max = Column(String(50), nullable=True)
    result_score_scaled = Column(String(50), nullable=True)
    result_success = Column(Boolean, nullable=True)
    result_completion = Column(Boolean, nullable=True)
    result_duration = Column(String(50), nullable=True)
    result_response = Column(Text, nullable=True)
    result_extensions = Column(JSON, nullable=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    stored = Column(DateTime(timezone=True), nullable=False)

    # Original statement storage (full JSON)
    statement = Column(JSON, nullable=False)

    # Game-specific parsed fields (for easy querying)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True, index=True)
    game_id = Column(Integer, nullable=True, index=True)
    level_id = Column(Integer, nullable=True, index=True)
    segment_id = Column(Integer, nullable=True, index=True)

    # Relationships
    student = relationship("Student", back_populates="xapi_statements")

    __table_args__ = (
        Index("ix_xapi_statements_composite", "student_id", "game_id", "level_id"),
        Index("ix_xapi_statements_actor_timestamp", "actor_account_name", "timestamp"),
    )
