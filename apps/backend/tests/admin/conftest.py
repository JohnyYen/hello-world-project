# Admin-specific test fixtures and configuration
import pytest
import asyncio
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from types import ModuleType
from typing import Optional

# Mock sqladmin before importing anything that depends on it
sqladmin_mock = ModuleType("sqladmin")
sqladmin_mock.Admin = MagicMock()
sqladmin_mock.ModelView = MagicMock()
sqladmin_mock.AdminView = MagicMock()
sys.modules["sqladmin"] = sqladmin_mock

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.base import Base
from src.users.domain.user import User
from src.users.domain.role import Role
from src.auth.infrastructure.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)


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
async def admin_test_db():
    """Create a test database session for admin tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = TestSessionLocal()
    yield session

    await session.close()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def admin_test_session(admin_test_db: AsyncSession):
    """Create a test session for individual tests with automatic cleanup."""
    yield admin_test_db
    await admin_test_db.rollback()


@pytest.fixture
def admin_role():
    """Create a mock admin Role."""
    role = MagicMock(spec=Role)
    role.id = "role-admin-001"
    role.role_name = "admin"
    role.description = "Administrator"
    return role


@pytest.fixture
def professor_role():
    """Create a mock professor Role."""
    role = MagicMock(spec=Role)
    role.id = "role-professor-001"
    role.role_name = "professor"
    role.description = "Professor"
    return role


@pytest.fixture
def student_role():
    """Create a mock student Role."""
    role = MagicMock(spec=Role)
    role.id = "role-student-001"
    role.role_name = "student"
    role.description = "Student"
    return role


@pytest.fixture
def mock_admin_user(admin_role):
    """Create a mock admin User object."""
    user = MagicMock(spec=User)
    user.id = 1
    user.username = "admin_user"
    user.email = "admin@example.com"
    user.hashed_password = get_password_hash("AdminPass123!")
    user.name = "Admin"
    user.lastname = "User"
    user.is_active = True
    user.is_deleted = False
    user.role_id = admin_role.id
    user.role = admin_role
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = None
    user.deleted_at = None
    return user


@pytest.fixture
def mock_professor_user(professor_role):
    """Create a mock professor User object."""
    user = MagicMock(spec=User)
    user.id = 2
    user.username = "professor_user"
    user.email = "professor@example.com"
    user.hashed_password = get_password_hash("ProfessorPass123!")
    user.name = "Professor"
    user.lastname = "User"
    user.is_active = True
    user.is_deleted = False
    user.role_id = professor_role.id
    user.role = professor_role
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = None
    user.deleted_at = None
    return user


@pytest.fixture
def mock_student_user(student_role):
    """Create a mock student User object."""
    user = MagicMock(spec=User)
    user.id = 3
    user.username = "student_user"
    user.email = "student@example.com"
    user.hashed_password = get_password_hash("StudentPass123!")
    user.name = "Student"
    user.lastname = "User"
    user.is_active = True
    user.is_deleted = False
    user.role_id = student_role.id
    user.role = student_role
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = None
    user.deleted_at = None
    return user


@pytest.fixture
def mock_inactive_admin_user(admin_role):
    """Create a mock inactive admin User object."""
    user = MagicMock(spec=User)
    user.id = 4
    user.username = "inactive_admin"
    user.email = "inactive_admin@example.com"
    user.hashed_password = get_password_hash("AdminPass123!")
    user.name = "Inactive"
    user.lastname = "Admin"
    user.is_active = False
    user.is_deleted = False
    user.role_id = admin_role.id
    user.role = admin_role
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = None
    user.deleted_at = None
    return user


@pytest.fixture
def valid_admin_token(mock_admin_user):
    """Generate a valid JWT token for admin user."""
    expires = timedelta(minutes=30)
    return create_access_token(
        data={"sub": mock_admin_user.username, "email": mock_admin_user.email},
        expires_delta=expires
    )


@pytest.fixture
def valid_professor_token(mock_professor_user):
    """Generate a valid JWT token for professor user."""
    expires = timedelta(minutes=30)
    return create_access_token(
        data={"sub": mock_professor_user.username, "email": mock_professor_user.email},
        expires_delta=expires
    )


@pytest.fixture
def expired_token():
    """Generate an expired JWT token."""
    expires = timedelta(seconds=-1)
    return create_access_token(
        data={"sub": "testuser", "email": "test@example.com"},
        expires_delta=expires
    )


@pytest.fixture
def mock_session_factory():
    """Mock session factory for async context."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()
    return mock_session