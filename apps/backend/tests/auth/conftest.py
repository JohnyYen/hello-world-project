# Auth-specific test fixtures and configuration
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
async def auth_test_db():
    """
    Create a test database session for auth tests and clean up after tests.
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
async def auth_test_session(auth_test_db: AsyncSession):
    """Create a test session for individual tests with automatic cleanup."""
    yield auth_test_db
    # Rollback any uncommitted changes
    await auth_test_db.rollback()


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


@pytest.fixture
def mock_inactive_user(sample_user_dict):
    """Create a mock inactive User object."""
    user = MagicMock(spec=User)
    user.id = 2
    user.username = "inactive_user"
    user.email = "inactive@example.com"
    user.hashed_password = sample_user_dict["hashed_password"]
    user.name = "Inactive"
    user.lastname = "User"
    user.is_active = False
    user.is_deleted = False
    user.role = MagicMock()
    user.role.role_name = "professor"
    return user


@pytest.fixture
def mock_deleted_user(sample_user_dict):
    """Create a mock deleted User object."""
    user = MagicMock(spec=User)
    user.id = 3
    user.username = "deleted_user"
    user.email = "deleted@example.com"
    user.hashed_password = sample_user_dict["hashed_password"]
    user.name = "Deleted"
    user.lastname = "User"
    user.is_active = False
    user.is_deleted = True
    user.deleted_at = datetime.now(timezone.utc)
    user.role = MagicMock()
    user.role.role_name = "professor"
    return user


# ============== Password Fixtures ==============


@pytest.fixture
def valid_password():
    """A valid password meeting all requirements."""
    return "SecurePass123!"


@pytest.fixture
def invalid_password_short():
    """Password too short (less than 8 characters)."""
    return "Short1!"


@pytest.fixture
def invalid_password_no_uppercase():
    """Password without uppercase letters."""
    return "lowercase123!"


@pytest.fixture
def invalid_password_no_lowercase():
    """Password without lowercase letters."""
    return "UPPERCASE123!"


@pytest.fixture
def invalid_password_no_number():
    """Password without numbers."""
    return "NoNumbers!!"


@pytest.fixture
def password_minimum_8_chars():
    """Password with exactly 8 characters (minimum)."""
    return "Pass1234"


@pytest.fixture
def password_exactly_8_chars():
    """Password with exactly 8 characters including uppercase, lowercase, number."""
    return "Ab123456"


# ============== JWT Token Fixtures ==============


@pytest.fixture
def valid_jwt_payload():
    """Valid JWT payload data."""
    return {"sub": "testuser", "email": "test@example.com"}


@pytest.fixture
def expired_jwt_payload():
    """Expired JWT payload data."""
    return {"sub": "testuser", "email": "test@example.com"}


@pytest.fixture
def generate_valid_token(valid_jwt_payload):
    """Generate a valid JWT token."""
    expires = timedelta(minutes=30)
    return create_access_token(data=valid_jwt_payload, expires_delta=expires)


@pytest.fixture
def generate_expired_token(expired_jwt_payload):
    """Generate an expired JWT token."""
    expires = timedelta(seconds=-1)  # Already expired
    return create_access_token(data=expired_jwt_payload, expires_delta=expires)


# ============== LMS Credential Fixtures ==============


@pytest.fixture
def sample_lms_credential_data():
    """Provide valid LMS credential data."""
    return {
        "lms_email": "student@university.edu",
        "lms_password": "lms_password123",
        "lms_provider": "moodle",
        "access_token": "lms_access_token",
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
    cred.acces_token = sample_lms_credential_data["access_token"]
    cred.expire_at = sample_lms_credential_data["expire_at"]
    return cred


# ============== Mock Repositories and Services ==============


@pytest.fixture
def mock_user_repository():
    """Create a mock UserRepository."""
    repo = MagicMock()
    repo.authenticate = AsyncMock()
    repo.get_by_email = AsyncMock()
    repo.get_by_username = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_user_service():
    """Create a mock UserService."""
    service = MagicMock()
    service.get_by_id = AsyncMock()
    service.update = AsyncMock()
    service.create_user = AsyncMock()
    return service


@pytest.fixture
def mock_lms_credential_repository():
    """Create a mock LMSCredentialRepository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_one_by_filters = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


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
