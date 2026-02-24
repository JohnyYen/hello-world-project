"""
Unit tests for LMSCredentialRepository.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users.infrastructure.lms_credential_repository import LMSCredentialRepository
from src.users.domain.lms_credential import LMSCredential


class TestLMSCredentialRepositoryInitialization:
    """Test suite for LMSCredentialRepository initialization."""

    @pytest.mark.asyncio
    async def test_repository_can_be_instantiated(self):
        """Test that LMSCredentialRepository can be instantiated."""
        mock_db = MagicMock(spec=AsyncSession)
        repo = LMSCredentialRepository(mock_db)

        assert repo.model == LMSCredential

    @pytest.mark.asyncio
    async def test_repository_inherits_from_base_repository(self):
        """Test that LMSCredentialRepository inherits from BaseRepository."""
        from src.shared.infrastructure.repositories.base_repository import (
            BaseRepository,
        )

        mock_db = MagicMock(spec=AsyncSession)
        repo = LMSCredentialRepository(mock_db)

        assert isinstance(repo, BaseRepository)


class TestLMSCredentialRepositoryGetByLmsEmail:
    """Test suite for LMSCredentialRepository.get_by_lms_email()."""

    @pytest.mark.asyncio
    async def test_get_by_lms_email_returns_credential(self):
        """Test that get_by_lms_email returns a credential when found."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_credential = MagicMock(spec=LMSCredential)
        mock_credential.lms_email = "test@university.edu"

        repo = LMSCredentialRepository(mock_db)
        repo.get_one_by_filters = AsyncMock(return_value=mock_credential)

        result = await repo.get_by_lms_email("test@university.edu")

        assert result == mock_credential
        repo.get_one_by_filters.assert_called_once_with(
            {"lms_email": "test@university.edu"}
        )

    @pytest.mark.asyncio
    async def test_get_by_lms_email_returns_none_when_not_found(self):
        """Test that get_by_lms_email returns None when not found."""
        mock_db = MagicMock(spec=AsyncSession)

        repo = LMSCredentialRepository(mock_db)
        repo.get_one_by_filters = AsyncMock(return_value=None)

        result = await repo.get_by_lms_email("nonexistent@university.edu")

        assert result is None


class TestLMSCredentialRepositoryGetByUserId:
    """Test suite for LMSCredentialRepository.get_by_user_id()."""

    @pytest.mark.asyncio
    async def test_get_by_user_id_returns_credential(self):
        """Test that get_by_user_id returns a credential when found."""
        mock_db = MagicMock(spec=AsyncSession)
        mock_credential = MagicMock(spec=LMSCredential)
        mock_credential.id = 1
        mock_credential.user_id = 123
        mock_credential.lms_email = "test@university.edu"

        # Mock the execute method with join query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=mock_credential)
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = LMSCredentialRepository(mock_db)

        result = await repo.get_by_user_id(123)

        assert result == mock_credential
        # Verify execute was called with join query
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_user_id_returns_none_when_not_found(self):
        """Test that get_by_user_id returns None when not found."""
        mock_db = MagicMock(spec=AsyncSession)

        # Mock the execute method returning None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)

        repo = LMSCredentialRepository(mock_db)

        result = await repo.get_by_user_id(999)

        assert result is None
        mock_db.execute.assert_called_once()


class TestLMSCredentialRepositoryGetByProvider:
    """Test suite for LMSCredentialRepository.get_by_provider()."""

    @pytest.mark.asyncio
    async def test_get_by_provider_returns_list(self):
        """Test that get_by_provider returns a list of credentials."""
        mock_db = MagicMock(spec=AsyncSession)

        mock_credential1 = MagicMock(spec=LMSCredential)
        mock_credential2 = MagicMock(spec=LMSCredential)

        repo = LMSCredentialRepository(mock_db)
        repo.get_by_filters = AsyncMock(
            return_value=[mock_credential1, mock_credential2]
        )

        result = await repo.get_by_provider("moodle")

        assert len(result) == 2
        repo.get_by_filters.assert_called_once_with({"lms_provider": "moodle"})


class TestLMSCredentialRepositoryModelFieldAnalysis:
    """Analysis tests to document the actual LMSCredential model fields."""

    def test_lms_credential_model_has_expected_fields(self):
        """Verify LMSCredential model has expected fields."""
        expected_fields = [
            "id",
            "lms_email",
            "lms_password",
            "lms_provider",
            "lms_url",
            "access_token",
            "refresh_token",
            "expire_at",
            "created_at",
            "updated_at",
            "user",  # Relationship field
        ]

        for field_name in expected_fields:
            assert hasattr(LMSCredential, field_name), (
                f"LMSCredential should have '{field_name}' field"
            )
