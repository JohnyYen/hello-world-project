# Test configuration file for pytest
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.base import Base
from src.shared.infrastructure.config import settings


# Test database URL (in-memory SQLite for isolation)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
async def test_db():
    """
    Create a test database session and clean up after tests.
    """
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
async def test_client(test_db: AsyncSession):
    """
    Create a test HTTP client with test database.
    """
    from main import app
    from src.shared.infrastructure.session import get_db

    # Override get_db to use test database
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """
    Provide valid test user data.
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "role_id": None,
    }


@pytest.fixture
def invalid_password_data():
    """
    Provide invalid password test data (missing requirements).
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "weak",  # Too short, no uppercase, no number
        "role_id": None,
    }


@pytest.fixture
def short_username_data():
    """
    Provide test data with username too short (< 3 chars).
    """
    return {
        "username": "ab",  # Only 2 chars
        "email": "test@example.com",
        "password": "TestPassword123!",
        "role_id": None,
    }


@pytest.fixture
def long_username_data():
    """
    Provide test data with username too long (> 100 chars).
    """
    return {
        "username": "a" * 101,  # 101 chars
        "email": "test@example.com",
        "password": "TestPassword123!",
        "role_id": None,
    }
