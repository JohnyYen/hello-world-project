# Game-specific test fixtures and configuration
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.shared.infrastructure.base import Base
from src.game.domain.game import Game
from src.game.domain.level import Level
from src.game.domain.segment_level import SegmentLevel
from src.game.domain.game_instance import GameInstance


# Test database URL (in-memory SQLite for isolation)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def game_test_db():
    """Create a test database session for game tests and clean up after tests."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    session = TestSessionLocal()

    yield session

    # Clean up
    await session.close()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def game_test_session(game_test_db: AsyncSession):
    """Create a test session for individual tests with automatic cleanup."""
    yield game_test_db
    # Rollback any uncommitted changes
    await game_test_db.rollback()


# ============== Game Fixtures ==============


@pytest.fixture
def sample_game_data():
    """Provide valid test game data."""
    return {
        "title": "Juego de Matemáticas",
        "description": "Aprende matemáticas básicas",
        "creator": "Profesor García",
        "subject": "Matemáticas",
        "publication_status": "published",
    }


@pytest.fixture
def mock_game(sample_game_data):
    """Create a mock Game object."""
    game = MagicMock(spec=Game)
    game.id = 1
    game.title = sample_game_data["title"]
    game.description = sample_game_data["description"]
    game.creator = sample_game_data["creator"]
    game.subject = sample_game_data["subject"]
    game.publication_status = sample_game_data["publication_status"]
    game.created_at = datetime.now(timezone.utc)
    game.updated_at = None
    game.deleted_at = None
    game.is_deleted = False
    game.levels = []
    return game


@pytest.fixture
def mock_game_with_levels(sample_game_data):
    """Create a mock Game object with levels."""
    game = MagicMock(spec=Game)
    game.id = 1
    game.title = sample_game_data["title"]
    game.description = sample_game_data["description"]
    game.creator = sample_game_data["creator"]
    game.subject = sample_game_data["subject"]
    game.publication_status = sample_game_data["publication_status"]
    game.created_at = datetime.now(timezone.utc)
    game.updated_at = None
    game.deleted_at = None
    game.is_deleted = False

    # Add mock levels
    level1 = MagicMock(spec=Level)
    level1.id = 1
    level1.level_number = 1
    level1.title = "Nivel 1"
    level1.segments = []

    level2 = MagicMock(spec=Level)
    level2.id = 2
    level2.level_number = 2
    level2.title = "Nivel 2"
    level2.segments = []

    game.levels = [level1, level2]
    return game


@pytest.fixture
def mock_deleted_game(sample_game_data):
    """Create a mock deleted Game object."""
    game = MagicMock(spec=Game)
    game.id = 2
    game.title = sample_game_data["title"]
    game.description = sample_game_data["description"]
    game.creator = sample_game_data["creator"]
    game.subject = sample_game_data["subject"]
    game.publication_status = sample_game_data["publication_status"]
    game.created_at = datetime.now(timezone.utc)
    game.updated_at = None
    game.deleted_at = datetime.now(timezone.utc)
    game.is_deleted = True
    game.levels = []
    return game


# ============== Level Fixtures ==============


@pytest.fixture
def sample_level_data():
    """Provide valid test level data."""
    return {
        "level_number": 1,
        "title": "Nivel 1: Introducción",
        "description": "Conceptos básicos",
        "goal": "Aprender sumas",
        "game_id": 1,
    }


@pytest.fixture
def mock_level(sample_level_data):
    """Create a mock Level object."""
    level = MagicMock(spec=Level)
    level.id = 1
    level.level_number = sample_level_data["level_number"]
    level.title = sample_level_data["title"]
    level.description = sample_level_data["description"]
    level.goal = sample_level_data["goal"]
    level.game_id = sample_level_data["game_id"]
    level.created_at = datetime.now(timezone.utc)
    level.updated_at = None
    level.deleted_at = None
    level.is_deleted = False
    level.segments = []
    return level


@pytest.fixture
def mock_level_with_segments(sample_level_data):
    """Create a mock Level object with segments."""
    level = MagicMock(spec=Level)
    level.id = 1
    level.level_number = sample_level_data["level_number"]
    level.title = sample_level_data["title"]
    level.description = sample_level_data["description"]
    level.goal = sample_level_data["goal"]
    level.game_id = sample_level_data["game_id"]
    level.created_at = datetime.now(timezone.utc)
    level.updated_at = None
    level.deleted_at = None
    level.is_deleted = False

    # Add mock segments
    segment1 = MagicMock(spec=SegmentLevel)
    segment1.id = 1
    segment1.configuration = {"type": "test"}

    segment2 = MagicMock(spec=SegmentLevel)
    segment2.id = 2
    segment2.configuration = {"type": "exercise"}

    level.segments = [segment1, segment2]
    return level


# ============== SegmentLevel Fixtures ==============


@pytest.fixture
def sample_segment_data():
    """Provide valid test segment level data."""
    return {
        "level_number_id": 1,
        "configuration": {"type": "test", "duration": 300},
    }


@pytest.fixture
def mock_segment(sample_segment_data):
    """Create a mock SegmentLevel object."""
    segment = MagicMock(spec=SegmentLevel)
    segment.id = 1
    segment.level_number_id = sample_segment_data["level_number_id"]
    segment.configuration = sample_segment_data["configuration"]
    segment.created_at = datetime.now(timezone.utc)
    segment.updated_at = None
    segment.deleted_at = None
    segment.is_deleted = False
    return segment


# ============== GameInstance Fixtures ==============


@pytest.fixture
def sample_instance_data():
    """Provide valid test game instance data."""
    return {
        "game_id": 1,
        "student_id": 1,
        "status": "active",
    }


@pytest.fixture
def mock_instance(sample_instance_data):
    """Create a mock GameInstance object."""
    instance = MagicMock(spec=GameInstance)
    instance.id = 1
    instance.game_id = sample_instance_data["game_id"]
    instance.student_id = sample_instance_data["student_id"]
    instance.status = sample_instance_data["status"]
    instance.started_at = datetime.now(timezone.utc)
    instance.created_at = datetime.now(timezone.utc)
    instance.updated_at = None
    instance.deleted_at = None
    instance.is_deleted = False
    return instance


@pytest.fixture
def mock_instance_with_relations(sample_instance_data, mock_game, mock_level):
    """Create a mock GameInstance object with game and student loaded."""
    instance = MagicMock(spec=GameInstance)
    instance.id = 1
    instance.game_id = sample_instance_data["game_id"]
    instance.student_id = sample_instance_data["student_id"]
    instance.status = sample_instance_data["status"]
    instance.started_at = datetime.now(timezone.utc)
    instance.created_at = datetime.now(timezone.utc)
    instance.updated_at = None
    instance.deleted_at = None
    instance.is_deleted = False

    # Add mock relations
    instance.game = mock_game
    instance.student = MagicMock()
    instance.student.user = MagicMock()
    instance.student.user.username = "test_student"

    return instance


# ============== Mock Repositories ==============


@pytest.fixture
def mock_game_repository():
    """Create a mock GameRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_id_with_levels = AsyncMock()
    repo.get_all = AsyncMock()
    repo.get_all_with_levels = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_level_repository():
    """Create a mock LevelRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_id_with_segments = AsyncMock()
    repo.get_by_game_id = AsyncMock()
    repo.get_by_game_id_with_segments = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_segment_repository():
    """Create a mock SegmentLevelRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_level_id = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_instance_repository():
    """Create a mock GameInstanceRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_id_with_relations = AsyncMock()
    repo.get_by_game_id = AsyncMock()
    repo.get_all_with_relations = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo
