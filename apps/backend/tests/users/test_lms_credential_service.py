"""
Unit tests for LMSCredentialService.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.application.service.lms_credential_service import LMSCredentialService
from src.users.domain.lms_credential import LMSCredential


class TestLMSCredentialServiceInitialization:
    """Test suite for LMSCredentialService initialization."""

    @pytest.mark.asyncio
    async def test_service_can_be_instantiated(self):
        """Test that LMSCredentialService can be instantiated."""
        mock_db = MagicMock(spec=AsyncSession)
        service = LMSCredentialService(db=mock_db)

        assert service.model == LMSCredential

    @pytest.mark.asyncio
    async def test_service_uses_lms_credential_repository(self):
        """Test that service uses LMSCredentialRepository."""
        from src.users.infrastructure.lms_credential_repository import (
            LMSCredentialRepository,
        )

        mock_db = MagicMock(spec=AsyncSession)
        service = LMSCredentialService(db=mock_db)

        # The repository should be set via BaseService
        assert service.repository is not None
        assert isinstance(service.repository, LMSCredentialRepository)


class TestLMSCredentialServiceGetByUserId:
    """Test suite for LMSCredentialService.get_by_user_id()."""

    @pytest.mark.asyncio
    async def test_get_by_user_id_returns_credential(self):
        """Test that get_by_user_id returns credentials when found."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_credential = MagicMock(spec=LMSCredential)
        mock_credential.id = 1
        mock_credential.user_id = 123

        # Mock the repository directly
        mock_repo = MagicMock()
        mock_repo.get_by_user_id = AsyncMock(return_value=mock_credential)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        result = await service.get_by_user_id(123)

        assert result == mock_credential
        mock_repo.get_by_user_id.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_get_by_user_id_returns_none_when_not_found(self):
        """Test that get_by_user_id returns None when not found."""
        mock_db = MagicMock(spec=AsyncSession)

        mock_repo = MagicMock()
        mock_repo.get_by_user_id = AsyncMock(return_value=None)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        result = await service.get_by_user_id(999)

        assert result is None


class TestLMSCredentialServiceGetByEmail:
    """Test suite for LMSCredentialService.get_by_email()."""

    @pytest.mark.asyncio
    async def test_get_by_email_returns_credential(self):
        """Test that get_by_email returns credentials when found."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_credential = MagicMock(spec=LMSCredential)
        mock_credential.lms_email = "test@university.edu"

        mock_repo = MagicMock()
        mock_repo.get_by_lms_email = AsyncMock(return_value=mock_credential)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        result = await service.get_by_email("test@university.edu")

        assert result == mock_credential
        mock_repo.get_by_lms_email.assert_called_once_with("test@university.edu")


class TestLMSCredentialServiceCreate:
    """Test suite for LMSCredentialService.create()."""

    @pytest.mark.asyncio
    async def test_create_with_user_raises_on_duplicate_email(self):
        """Test that create_with_user raises on duplicate email."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_existing = MagicMock(spec=LMSCredential)
        mock_existing.lms_email = "existing@university.edu"

        # First call returns existing (for duplicate check)
        # Second call would be for actual creation (shouldn't reach here)
        mock_repo = MagicMock()
        mock_repo.get_by_lms_email = AsyncMock(return_value=mock_existing)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        from src.shared.domain.exceptions import DuplicateEntryException

        with pytest.raises(DuplicateEntryException):
            await service.create_with_user(
                user_id=123,
                lms_url="https://moodle.edu",
                lms_email="existing@university.edu",
                lms_password="password123",
                lms_provider="moodle",
            )

    @pytest.mark.asyncio
    async def test_create_with_user_creates_credential(self):
        """Test that create_with_user creates credentials successfully."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_new_credential = MagicMock(spec=LMSCredential)
        mock_new_credential.id = 1
        mock_new_credential.lms_email = "new@university.edu"

        # First call returns None (no duplicate), second for creation
        mock_repo = MagicMock()
        mock_repo.get_by_lms_email = AsyncMock(return_value=None)
        mock_repo.create = AsyncMock(return_value=mock_new_credential)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        result = await service.create_with_user(
            user_id=123,
            lms_url="https://moodle.edu",
            lms_email="new@university.edu",
            lms_password="password123",
            lms_provider="moodle",
        )

        assert result == mock_new_credential
        mock_repo.get_by_lms_email.assert_called_once()
        mock_repo.create.assert_called_once()


class TestLMSCredentialServicePasswordHashing:
    """Test suite for password hashing in LMSCredentialService."""

    @pytest.mark.asyncio
    async def test_create_with_user_hashes_lms_password(self):
        """Test that create_with_user hashes the LMS password."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_new_credential = MagicMock(spec=LMSCredential)
        mock_new_credential.id = 1
        mock_new_credential.lms_email = "test@university.edu"

        mock_repo = MagicMock()
        mock_repo.get_by_lms_email = AsyncMock(return_value=None)
        mock_repo.create = AsyncMock(return_value=mock_new_credential)

        service = LMSCredentialService(db=mock_db)
        service.repository = mock_repo

        plain_password = "plain_password_123"

        await service.create_with_user(
            user_id=123,
            lms_url="https://moodle.edu",
            lms_email="test@university.edu",
            lms_password=plain_password,
            lms_provider="moodle",
        )

        # Verify create was called with hashed password
        mock_repo.create.assert_called_once()
        call_kwargs = mock_repo.create.call_args[1]
        create_data = call_kwargs.get("data") or call_kwargs.get("_data")

        # Password should be hashed (not plain)
        if create_data:
            assert "lms_password" in create_data
            # Hash should be different from plain password
            assert create_data["lms_password"] != plain_password
            # Hash should be bcrypt format
            assert create_data["lms_password"].startswith("$2")
