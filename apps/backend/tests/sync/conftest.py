# Sync-specific test fixtures and configuration
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.shared.infrastructure.base import Base
from src.sync.domain.sync_session import SyncSession
from src.sync.domain.sync_event import SyncEvent


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

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
async def sync_test_db():
    """Create a test database session for sync tests and clean up after tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = TestSessionLocal()

    yield session

    await session.close()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def sync_test_session(sync_test_db: AsyncSession):
    """Create a test session for individual tests with automatic cleanup."""
    yield sync_test_db
    await sync_test_db.rollback()


# ============== Sync Session Fixtures ==============


@pytest.fixture
def sample_session_data():
    """Provide valid test sync session data."""
    return {
        "instance_id": 1,
        "start_time": datetime.now(timezone.utc),
        "end_time": None,
        "status": "active",
    }


@pytest.fixture
def mock_sync_session(sample_session_data):
    """Create a mock SyncSession object."""
    session = MagicMock(spec=SyncSession)
    session.id = 1
    session.instance_id = sample_session_data["instance_id"]
    session.start_time = sample_session_data["start_time"]
    session.end_time = sample_session_data["end_time"]
    session.status = sample_session_data["status"]
    session.is_deleted = False
    session.deleted_at = None
    return session


@pytest.fixture
def mock_ended_sync_session(sample_session_data):
    """Create a mock ended SyncSession object."""
    session = MagicMock(spec=SyncSession)
    session.id = 1
    session.instance_id = sample_session_data["instance_id"]
    session.start_time = sample_session_data["start_time"]
    session.end_time = datetime.now(timezone.utc)
    session.status = "completed"
    session.is_deleted = False
    session.deleted_at = None
    return session


# ============== Sync Event Fixtures ==============


@pytest.fixture
def sample_event_data():
    """Provide valid test sync event data."""
    return {
        "sync_session_id": 1,
        "event_type": "player_action",
        "payload": {"action": "move", "position": {"x": 10, "y": 20}},
    }


@pytest.fixture
def mock_sync_event(sample_event_data):
    """Create a mock SyncEvent object."""
    event = MagicMock(spec=SyncEvent)
    event.id = 1
    event.sync_session_id = sample_event_data["sync_session_id"]
    event.event_type = sample_event_data["event_type"]
    event.payload = sample_event_data["payload"]
    event.timestamp = datetime.now(timezone.utc)
    event.status = "pending"
    event.is_deleted = False
    event.deleted_at = None
    return event


# ============== Mock Repositories ==============


@pytest.fixture
def mock_sync_session_repository():
    """Create a mock SyncSessionRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_filters = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.exists = AsyncMock()
    return repo


@pytest.fixture
def mock_sync_event_repository():
    """Create a mock SyncEventRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_filters = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


# ============== Exception Fixtures ==============


@pytest.fixture
def mock_not_found_exception():
    """Mock NotFoundException."""
    from src.shared.domain.exceptions import NotFoundException

    return NotFoundException("Recurso no encontrado")
