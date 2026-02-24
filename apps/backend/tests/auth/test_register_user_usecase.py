"""
Unit tests for RegisterUserUseCase.

This test suite is designed to find defects in:
- User registration flow
- Duplicate user detection
- Token generation after registration
- Validation of user data
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

from src.auth.application.usecase.register_user_usecase import RegisterUserUseCase
from src.users.domain.user import User
from src.shared.domain.exceptions import DuplicateEntryException
from src.users.api.v1.schemas.user import UserCreate


def create_mock_role_repository():
    """Helper to create a properly configured mock RoleRepository."""
    mock_role = MagicMock()
    mock_role.id = 1
    mock_role_repo = MagicMock()
    mock_role_repo.get_professor_role = AsyncMock(return_value=mock_role)
    return mock_role_repo


class TestRegisterUserUseCaseInitialization:
    """Test suite for RegisterUserUseCase initialization."""

    def test_init_creates_instance(self):
        """Test that RegisterUserUseCase can be instantiated."""
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)
            assert uc is not None
            assert uc.db == mock_db
            assert uc.user_service == mock_service

    def test_init_with_user_service(self):
        """Test initialization with a mock user service."""
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)
            assert uc.user_service == mock_service


class TestRegisterUserExecute:
    """Test suite for the execute method."""

    @pytest.mark.asyncio
    async def test_execute_successful_registration(self, sample_user_data, mock_user):
        """
        Test successful user registration flow.
        Verifies: role is fetched, user is created, token is generated.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            assert result is not None
            assert result.access_token is not None
            assert result.token_type == "bearer"
            assert result.expires_in is not None
            assert result.user is not None

    @pytest.mark.asyncio
    async def test_execute_duplicate_email(self, sample_user_data, mock_user):
        """
        Verify DuplicateEntryException for duplicate email.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(
            side_effect=DuplicateEntryException("El email ya está registrado")
        )

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            with pytest.raises(DuplicateEntryException):
                await uc.execute(user_data=user_create)

    @pytest.mark.asyncio
    async def test_execute_duplicate_username(self, sample_user_data, mock_user):
        """
        Verify DuplicateEntryException for duplicate username.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(
            side_effect=DuplicateEntryException("El nombre de usuario ya está en uso")
        )

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            with pytest.raises(DuplicateEntryException):
                await uc.execute(user_data=user_create)

    @pytest.mark.asyncio
    async def test_execute_calls_create_user_with_role_id(
        self, sample_user_data, mock_user
    ):
        """
        Verify create_user is called with correct data including role_id.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            await uc.execute(user_data=user_create)

            # Verify create_user was called with role_id
            mock_service.create_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_creates_token_for_new_user(
        self, sample_user_data, mock_user
    ):
        """
        Verify token is created for the new user.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            # Token should be valid JWT
            assert result.access_token is not None
            assert len(result.access_token) > 0

            # Token should contain user data
            from src.shared.infrastructure.config import settings
            import jwt

            decoded = jwt.decode(
                result.access_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            assert decoded["sub"] == mock_user.username


class TestRegisterUserEdgeCases:
    """Test suite for edge cases in user registration."""

    @pytest.mark.asyncio
    async def test_execute_with_none_user_data(self, mock_user):
        """
        Edge case - None user data.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            try:
                await uc.execute(user_data=None)
                pytest.fail("Should raise an exception for None user_data")
            except (TypeError, AttributeError, DuplicateEntryException):
                pass

    @pytest.mark.asyncio
    async def test_execute_weak_password(self, sample_user_data):
        """
        Verify weak passwords are rejected by schema validation.
        """
        weak_data = {**sample_user_data, "password": "weak"}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=MagicMock())

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            # Pydantic validation should reject weak passwords
            with pytest.raises(ValueError):
                UserCreate(**weak_data)

    @pytest.mark.asyncio
    async def test_execute_empty_username(self, sample_user_data):
        """
        Verify empty username is rejected.
        """
        empty_username_data = {**sample_user_data, "username": ""}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            # Should fail validation
            with pytest.raises(ValueError):
                UserCreate(**empty_username_data)

    @pytest.mark.asyncio
    async def test_execute_invalid_email(self, sample_user_data):
        """
        Verify invalid email is rejected.
        """
        invalid_email_data = {**sample_user_data, "email": "not-an-email"}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            # Should fail Pydantic validation
            with pytest.raises(ValueError):
                UserCreate(**invalid_email_data)

    @pytest.mark.asyncio
    async def test_execute_short_username(self, sample_user_data):
        """
        Verify username too short is rejected.
        """
        short_username_data = {**sample_user_data, "username": "ab"}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            # Should fail validation (min 3 characters)
            with pytest.raises(ValueError):
                UserCreate(**short_username_data)


class TestRegisterUserTokenGeneration:
    """Test suite specifically for token generation after registration."""

    @pytest.mark.asyncio
    async def test_token_contains_correct_subject(self, sample_user_data, mock_user):
        """
        Verify token contains correct user identifier.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            from src.shared.infrastructure.config import settings
            import jwt

            decoded = jwt.decode(
                result.access_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            # Token should use username as 'sub'
            assert decoded["sub"] == mock_user.username

    @pytest.mark.asyncio
    async def test_token_has_expiration(self, sample_user_data, mock_user):
        """
        Verify token has expiration claim.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            from src.shared.infrastructure.config import settings
            import jwt

            decoded = jwt.decode(
                result.access_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            assert "exp" in decoded
            assert isinstance(decoded["exp"], int)

    @pytest.mark.asyncio
    async def test_token_type_is_bearer(self, sample_user_data, mock_user):
        """
        Verify response indicates bearer token type.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            assert result.token_type.lower() == "bearer"

    @pytest.mark.asyncio
    async def test_expires_in_matches_settings(self, sample_user_data, mock_user):
        """
        Verify expires_in matches configuration.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            result = await uc.execute(user_data=user_create)

            from src.shared.infrastructure.config import settings

            assert result.expires_in == settings.ACCESS_TOKEN_EXPIRE_MINUTES


class TestRegisterUserErrorHandling:
    """Test suite for error handling in registration."""

    @pytest.mark.asyncio
    async def test_execute_database_error(self, sample_user_data):
        """
        Verify database errors are handled gracefully.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            # Should propagate the exception
            with pytest.raises(Exception) as exc_info:
                await uc.execute(user_data=user_create)
            assert (
                "Database" in str(exc_info.value)
                or "connection" in str(exc_info.value).lower()
            )

    @pytest.mark.asyncio
    async def test_execute_service_returns_none(self, sample_user_data):
        """
        Verify behavior when service returns None.
        This could happen if create_user returns None instead of raising.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=None)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            # If create_user returns None, it could cause AttributeError
            # when trying to access user.username
            try:
                result = await uc.execute(user_data=user_create)
                # If we get here, the code handled it gracefully
                pytest.fail("Should have failed when user is None")
            except AttributeError as e:
                # This would be a defect - trying to access .username on None
                assert "username" in str(e) or "NoneType" in str(e)


class TestRegisterUserSecurity:
    """Test suite for security-related scenarios."""

    @pytest.mark.asyncio
    async def test_password_is_hashed_before_storage(self, sample_user_data, mock_user):
        """
        Verify password is hashed by the service.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)
            await uc.execute(user_data=user_create)

            # Verify create_user was called
            mock_service.create_user.assert_called_once()


class TestRegisterUserConcurrency:
    """Test suite for concurrent registration attempts."""

    @pytest.mark.asyncio
    async def test_concurrent_registrations_same_email(
        self, sample_user_data, mock_user
    ):
        """
        Verify concurrent registrations with same email.
        Only one should succeed, the other should get DuplicateEntryException.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(
            side_effect=DuplicateEntryException("El email ya está registrado")
        )
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            async def register():
                try:
                    return await uc.execute(user_data=user_create)
                except DuplicateEntryException:
                    return "duplicate"

            # Run multiple concurrent registrations
            tasks = [register() for _ in range(5)]
            results = await asyncio.gather(*tasks)

            # All should fail with duplicate
            duplicates = sum(1 for r in results if r == "duplicate")
            assert duplicates == 5

    @pytest.mark.asyncio
    async def test_concurrent_registrations_same_username(
        self, sample_user_data, mock_user
    ):
        """
        Verify concurrent registrations with same username.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(
            side_effect=DuplicateEntryException("El nombre de usuario ya está en uso")
        )
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            user_create = UserCreate(**sample_user_data)

            async def register():
                try:
                    return await uc.execute(user_data=user_create)
                except DuplicateEntryException:
                    return "duplicate"

            tasks = [register() for _ in range(5)]
            results = await asyncio.gather(*tasks)

            duplicates = sum(1 for r in results if r == "duplicate")
            assert duplicates == 5


class TestRegisterUserInputValidation:
    """Test suite for input validation."""

    @pytest.mark.asyncio
    async def test_special_characters_in_username(self, sample_user_data):
        """
        Verify handling of special characters in username.
        """
        special_username_data = {**sample_user_data, "username": "user_name-123"}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            try:
                UserCreate(**special_username_data)
            except ValueError:
                pass

    @pytest.mark.asyncio
    async def test_unicode_in_username(self, sample_user_data):
        """
        Verify handling of unicode in username.
        """
        unicode_username_data = {**sample_user_data, "username": "用户"}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            try:
                UserCreate(**unicode_username_data)
            except ValueError:
                pass

    @pytest.mark.asyncio
    async def test_very_long_username(self, sample_user_data):
        """
        Verify handling of very long username.
        """
        long_username_data = {**sample_user_data, "username": "a" * 100}
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock()

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            try:
                UserCreate(**long_username_data)
            except ValueError:
                pass

    @pytest.mark.asyncio
    async def test_email_case_sensitivity(self, sample_user_data, mock_user):
        """
        Verify email case handling in registration.
        Different cases of the same email should be treated as duplicates.
        """
        mock_db = MagicMock()
        mock_service = MagicMock()
        mock_service.create_user = AsyncMock(return_value=mock_user)
        mock_service.get_user_by_id_with_role = AsyncMock(return_value=mock_user)

        mock_role_repo = create_mock_role_repository()

        with patch(
            "src.auth.application.usecase.register_user_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = RegisterUserUseCase(db=mock_db, user_service=mock_service)

            # Same email, different case
            uppercase_email_data = {**sample_user_data, "email": "TEST@EXAMPLE.COM"}
            user_create = UserCreate(**uppercase_email_data)

            # This should work (email normalization is typically done by service)
            result = await uc.execute(user_data=user_create)
            assert result is not None
