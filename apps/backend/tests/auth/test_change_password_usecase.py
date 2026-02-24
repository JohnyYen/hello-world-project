"""
Unit tests for ChangePasswordUseCase.

This test suite is designed to find defects in:
- Password change validation logic
- Password strength requirements (minimum 8 characters)
- Current password verification
- Security vulnerabilities in password change flow
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from src.auth.application.usecase.change_password_usecase import (
    ChangePasswordUseCase,
    InvalidPasswordException,
)
from src.shared.domain.exceptions import (
    NotFoundException,
    InvalidCredentialsException,
)
from src.auth.infrastructure.security import get_password_hash, verify_password


class TestChangePasswordUseCaseInitialization:
    """Test suite for ChangePasswordUseCase initialization."""

    def test_init_creates_instance(self):
        """Test that ChangePasswordUseCase can be instantiated."""
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)
        assert uc is not None
        assert uc.user_service == mock_service

    def test_init_with_user_service(self):
        """Test initialization with a mock user service."""
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)
        assert uc.user_service == mock_service


class TestChangePasswordValidation:
    """Test suite for password strength validation (minimum 8 characters)."""

    def test_validate_password_minimum_length_8(self):
        """Test minimum password length validation (8 characters minimum)."""
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)

        # Exactly 8 characters should pass
        assert uc._validate_password_strength("Ab123456") is True

        # 7 characters should fail
        assert uc._validate_password_strength("Ab12345") is False

        # 8 characters should pass (no complexity requirements beyond length)
        assert uc._validate_password_strength("Pass1234") is True

    def test_validate_password_empty(self):
        """Test empty password validation."""
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)
        assert uc._validate_password_strength("") is False

    def test_validate_password_very_long(self):
        """Test very long password validation."""
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)
        long_password = "A" * 1000
        assert uc._validate_password_strength(long_password) is True

    def test_validate_password_only_numbers(self):
        """
        Password with only numbers but 8+ chars passes validation.
        Implementation only checks length (minimum 8 characters), not complexity.
        """
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)

        # This passes with the current implementation (only checks length)
        assert uc._validate_password_strength("12345678") is True

    def test_validate_password_only_lowercase(self):
        """
        Password with only lowercase but 8+ chars passes validation.
        Implementation only checks length (minimum 8 characters), not complexity.
        """
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)

        # This passes with the current implementation
        assert uc._validate_password_strength("password") is True

    def test_validate_password_only_uppercase(self):
        """
        Password with only uppercase but 8+ chars passes validation.
        Implementation only checks length (minimum 8 characters), not complexity.
        """
        mock_service = MagicMock()
        uc = ChangePasswordUseCase(user_service=mock_service)

        # This passes with the current implementation
        assert uc._validate_password_strength("PASSWORD") is True


class TestChangePasswordExecute:
    """Test suite for the execute method."""

    @pytest.mark.asyncio
    async def test_execute_successful_password_change(self, mock_user, valid_password):
        """
        Test successful password change with valid credentials.
        """
        new_password = "NewSecurePass456!"
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock(return_value=mock_user)

        uc = ChangePasswordUseCase(user_service=mock_service)

        result = await uc.execute(
            user_id=1, current_password=valid_password, new_password=new_password
        )

        assert result is True
        mock_service.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_user_not_found(self, valid_password):
        """
        Verify NotFoundException when user doesn't exist.
        """
        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=None)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(NotFoundException):
            await uc.execute(
                user_id=999,
                current_password=valid_password,
                new_password="NewPassword123!",
            )

    @pytest.mark.asyncio
    async def test_execute_wrong_current_password(self, mock_user, valid_password):
        """
        Verify InvalidCredentialsException for wrong password.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(InvalidCredentialsException):
            await uc.execute(
                user_id=1,
                current_password="WrongPassword123!",
                new_password="NewPassword123!",
            )

    @pytest.mark.asyncio
    async def test_execute_weak_new_password_length(self, mock_user, valid_password):
        """
        Verify InvalidPasswordException for passwords less than 8 characters.
        This is the only validation in the current implementation.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        # Passwords with less than 8 characters should fail
        weak_passwords = [
            "short",  # Too short (5 chars)
            "Ab1!@",  # Too short (5 chars)
            "1234567",  # 7 chars - still too short
        ]

        for weak_password in weak_passwords:
            with pytest.raises(InvalidPasswordException):
                await uc.execute(
                    user_id=1,
                    current_password=valid_password,
                    new_password=weak_password,
                )

    @pytest.mark.asyncio
    async def test_execute_empty_current_password(self, mock_user, valid_password):
        """
        Edge case - empty current password.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(InvalidCredentialsException):
            await uc.execute(
                user_id=1, current_password="", new_password="NewPassword123!"
            )

    @pytest.mark.asyncio
    async def test_execute_empty_new_password(self, mock_user, valid_password):
        """
        Edge case - empty new password.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(InvalidPasswordException):
            await uc.execute(
                user_id=1, current_password=valid_password, new_password=""
            )

    @pytest.mark.asyncio
    async def test_execute_none_current_password(self, mock_user, valid_password):
        """
        Edge case - None current password.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        try:
            await uc.execute(
                user_id=1, current_password=None, new_password="NewPassword123!"
            )
            pytest.fail("Should raise an exception for None password")
        except (InvalidCredentialsException, TypeError, AttributeError):
            pass

    @pytest.mark.asyncio
    async def test_execute_none_new_password(self, mock_user, valid_password):
        """
        Edge case - None new password.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        try:
            await uc.execute(
                user_id=1, current_password=valid_password, new_password=None
            )
            pytest.fail("Should raise an exception for None password")
        except (InvalidPasswordException, TypeError, AttributeError):
            pass


class TestChangePasswordSecurity:
    """Test suite for security-related scenarios."""

    @pytest.mark.asyncio
    async def test_new_password_same_as_current(self, mock_user, valid_password):
        """
        Current implementation allows same password.
        Only validates minimum 8 characters, not uniqueness.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        # Current behavior - allows same password
        result = await uc.execute(
            user_id=1, current_password=valid_password, new_password=valid_password
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_password_hash_is_updated(self, mock_user, valid_password):
        """
        Verify the password hash is properly updated.
        """
        old_password = "OldPassword123!"
        new_password = "NewSecurePass456!"

        mock_user.hashed_password = get_password_hash(old_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        await uc.execute(
            user_id=1, current_password=old_password, new_password=new_password
        )

        # Verify update was called
        mock_service.update.assert_called_once()
        call_args = mock_service.update.call_args
        update_data = call_args[0][1]

        assert "hashed_password" in update_data
        # The new hash should be different from old hash
        assert update_data["hashed_password"] != mock_user.hashed_password

    @pytest.mark.asyncio
    async def test_password_hash_is_properly_hashed(self, mock_user, valid_password):
        """
        Verify the new password is properly hashed.
        """
        old_password = "OldPassword123!"
        new_password = "NewSecurePass456!"

        mock_user.hashed_password = get_password_hash(old_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        await uc.execute(
            user_id=1, current_password=old_password, new_password=new_password
        )

        call_args = mock_service.update.call_args
        update_data = call_args[0][1]

        # Verify new hash is valid
        assert verify_password(new_password, update_data["hashed_password"])
        # Verify old password no longer matches
        assert not verify_password(old_password, update_data["hashed_password"])

    @pytest.mark.asyncio
    async def test_update_not_called_on_validation_failure(
        self, mock_user, valid_password
    ):
        """
        Verify update is not called if validation fails.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        try:
            await uc.execute(
                user_id=1,
                current_password=valid_password,
                new_password="weak",  # Too short
            )
        except InvalidPasswordException:
            pass

        # Update should not be called due to validation failure
        mock_service.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_not_called_on_user_not_found(self, valid_password):
        """
        Verify update is not called if user not found.
        """
        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=None)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        try:
            await uc.execute(
                user_id=999,
                current_password=valid_password,
                new_password="NewPassword123!",
            )
        except NotFoundException:
            pass

        # Update should not be called
        mock_service.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_not_called_on_wrong_password(self, mock_user, valid_password):
        """
        Verify update is not called if current password wrong.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        try:
            await uc.execute(
                user_id=1,
                current_password="WrongPassword123!",
                new_password="NewPassword123!",
            )
        except InvalidCredentialsException:
            pass

        # Update should not be called
        mock_service.update.assert_not_called()


class TestChangePasswordEdgeCases:
    """Test suite for edge cases."""

    @pytest.mark.asyncio
    async def test_negative_user_id(self, valid_password):
        """
        Edge case - negative user ID.
        """
        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=None)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(NotFoundException):
            await uc.execute(
                user_id=-1,
                current_password=valid_password,
                new_password="NewPassword123!",
            )

    @pytest.mark.asyncio
    async def test_zero_user_id(self, valid_password):
        """
        Edge case - zero user ID.
        """
        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=None)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        with pytest.raises(NotFoundException):
            await uc.execute(
                user_id=0,
                current_password=valid_password,
                new_password="NewPassword123!",
            )

    @pytest.mark.asyncio
    async def test_very_long_password(self, mock_user, valid_password):
        """
        Test handling of very long passwords.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        long_password = "A" * 1000

        # Should work if password is long enough (1000 > 8)
        result = await uc.execute(
            user_id=1, current_password=valid_password, new_password=long_password
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_unicode_password(self, mock_user, valid_password):
        """
        Test handling of unicode characters in passwords.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        unicode_password = "Contraseña_安全_🔐123"

        result = await uc.execute(
            user_id=1, current_password=valid_password, new_password=unicode_password
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_special_chars_password(self, mock_user, valid_password):
        """
        Test handling of special characters in passwords.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        special_password = "Pass!@#$%^&*()_+-=[]{}|;':\",./<>?123"

        result = await uc.execute(
            user_id=1, current_password=valid_password, new_password=special_password
        )
        assert result is True


class TestChangePasswordConcurrency:
    """Test suite for concurrent password change attempts."""

    @pytest.mark.asyncio
    async def test_concurrent_password_changes(self, mock_user, valid_password):
        """
        Verify concurrent password change requests.
        """
        mock_user.hashed_password = get_password_hash(valid_password)

        mock_service = MagicMock()
        mock_service.get_by_id = AsyncMock(return_value=mock_user)
        mock_service.update = AsyncMock()

        uc = ChangePasswordUseCase(user_service=mock_service)

        async def change_password():
            return await uc.execute(
                user_id=1,
                current_password=valid_password,
                new_password="NewPassword456!",
            )

        # Run multiple concurrent password changes
        tasks = [change_password() for _ in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # With mocks, all should succeed (no real database race conditions)
        # In production, only one should succeed (first one wins)
        successful = sum(1 for r in results if r is True)
        assert successful == 5  # All succeed with mocks
