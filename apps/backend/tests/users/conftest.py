# Users-specific test fixtures and configuration
import pytest
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.base import Base
from src.users.domain.lms_credential import LMSCredential
from src.users.domain.user import User
from src.users.domain.role import Role
from src.auth.infrastructure.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)


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
async def users_test_db():
    """
    Create a test database session for users tests and clean up after tests.
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
async def users_test_session(users_test_db: AsyncSession):
    """Create a test session for individual tests with automatic cleanup."""
    yield users_test_db
    # Rollback any uncommitted changes
    await users_test_db.rollback()


# ============== LMS Credential Fixtures ==============


@pytest.fixture
def sample_lms_credential_data():
    """Provide valid LMS credential data."""
    return {
        "lms_email": "student@university.edu",
        "lms_password": "lms_password123",
        "lms_provider": "moodle",
        "lms_url": "https://moodle.university.edu",
        "access_token": "lms_access_token",
        "refresh_token": "lms_refresh_token",
        "expire_at": datetime.now(timezone.utc) + timedelta(hours=1),
    }


@pytest.fixture
def mock_lms_credential(sample_lms_credential_data):
    """Create a mock LMSCredential object."""
    cred = MagicMock(spec=LMSCredential)
    cred.id = 1
    cred.lms_email = sample_lms_credential_data["lms_email"]
    cred.lms_password = sample_lms_credential_data["lms_password"]
    cred.lms_provider = sample_lms_credential_data["lms_provider"]
    cred.lms_url = sample_lms_credential_data["lms_url"]
    cred.access_token = sample_lms_credential_data["access_token"]
    cred.refresh_token = sample_lms_credential_data["refresh_token"]
    cred.expire_at = sample_lms_credential_data["expire_at"]
    cred.created_at = datetime.now(timezone.utc)
    cred.updated_at = None
    return cred


@pytest.fixture
def mock_lms_credential_repository():
    """Create a mock LMSCredentialRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_lms_email = AsyncMock()
    repo.get_by_user_id = AsyncMock()
    repo.get_one_by_filters = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.soft_delete = AsyncMock()
    return repo


# ============== User Fixtures ==============


@pytest.fixture
def sample_user_data():
    """Provide valid test user data for registration."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test",
        "lastname": "User",
        "role_id": None,
    }


@pytest.fixture
def sample_user_dict(sample_user_data):
    """Convert user data to dict format."""
    return {
        **sample_user_data,
        "hashed_password": get_password_hash(sample_user_data["password"]),
    }


@pytest.fixture
def mock_user(sample_user_dict):
    """Create a mock User object."""
    user = MagicMock(spec=User)
    user.id = 1
    user.username = sample_user_dict["username"]
    user.email = sample_user_dict["email"]
    user.hashed_password = sample_user_dict["hashed_password"]
    user.name = "Test"
    user.lastname = "User"
    user.is_active = True
    user.is_deleted = False
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = None
    user.deleted_at = None
    # Mock role for UserResponse validation
    user.role = MagicMock()
    user.role.role_name = "professor"
    return user


# ============== Exception Fixtures ==============


@pytest.fixture
def mock_invalid_credentials_exception():
    """Mock InvalidCredentialsException."""
    from src.shared.domain.exceptions import InvalidCredentialsException

    return InvalidCredentialsException("Credenciales inválidas")


@pytest.fixture
def mock_not_found_exception():
    """Mock NotFoundException."""
    from src.shared.domain.exceptions import NotFoundException

    return NotFoundException("Usuario no encontrado")


@pytest.fixture
def mock_duplicate_entry_exception():
    """Mock DuplicateEntryException."""
    from src.shared.domain.exceptions import DuplicateEntryException

    return DuplicateEntryException("El recurso ya existe")
