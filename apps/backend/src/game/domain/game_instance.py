from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from src.shared.infrastructure.base import Base
from src.shared.domain.enums import GameStatus


class GameInstance(Base):
    __tablename__ = "game_instances"

    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(SAEnum(GameStatus), nullable=True)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="game_instances")
    game = relationship("Game", back_populates="instances")
    course = relationship("Course")
    # Using string reference to avoid circular import with sync domain
    sync_sessions = relationship(
        "src.sync.domain.sync_session.SyncSession", back_populates="game_instance"
    )
