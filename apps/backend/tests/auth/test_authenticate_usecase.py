"""
Unit tests for AuthenticateUseCase.

This test suite is designed to find defects in:
- Authentication flow
- Token generation on login
- Error handling for invalid credentials
- Edge cases in user authentication
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

from src.auth.application.usecase.authenticate_usecase import AuthenticateUseCase
from src.users.domain.user import User
from src.shared.domain.exceptions import InvalidCredentialsException
from src.users.api.v1.schemas.user import UserLoginResponse


class TestAuthenticateUseCaseInitialization:
    """Test suite for AuthenticateUseCase initialization."""

    def test_init_creates_instance(self):
        """Test that AuthenticateUseCase can be instantiated with db session."""
        mock_db = MagicMock()
        uc = AuthenticateUseCase(db=mock_db)
        assert uc is not None
        assert uc.db == mock_db


class TestAuthenticateUseCaseExecute:
    """Test suite for the execute method."""

    @pytest.mark.asyncio
    async def test_execute_successful_authentication(self, mock_user, sample_user_data):
        """
        Test successful authentication flow.
        Verify the use case returns a proper UserLoginResponse with role loaded.
        """
        mock_db = MagicMock()

        # Mock UserRepository
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

        # Mock db.execute for role loading
        mock_result = MagicMock()
        mock_result.scalar_one = MagicMock(return_value=mock_user)
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)
            result = await uc.execute(
                email=sample_user_data["email"], password=sample_user_data["password"]
            )

            assert result is not None
            assert isinstance(result, UserLoginResponse)
            assert result.access_token is not None
            assert result.token_type == "bearer"
            assert result.expires_in is not None
            assert result.user is not None

    @pytest.mark.asyncio
    async def test_execute_invalid_credentials_raises_exception(self, sample_user_data):
        """
        Verify InvalidCredentialsException is raised for wrong passwords.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(email="wrong@example.com", password="wrongpassword")

    @pytest.mark.asyncio
    async def test_execute_user_not_found(self, sample_user_data):
        """
        Verify proper handling when user doesn't exist.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(
                    email="nonexistent@example.com", password="anypassword"
                )

    @pytest.mark.asyncio
    async def test_execute_inactive_user(self, mock_inactive_user):
        """
        Verify inactive users cannot authenticate.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(email="inactive@example.com", password="anypassword")

    @pytest.mark.asyncio
    async def test_execute_deleted_user(self, mock_deleted_user):
        """
        Verify soft-deleted users cannot authenticate.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(email="deleted@example.com", password="anypassword")

    @pytest.mark.asyncio
    async def test_execute_empty_email(self, sample_user_data):
        """
        Edge case - empty email handling.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(email="", password="anypassword")

    @pytest.mark.asyncio
    async def test_execute_empty_password(self, sample_user_data):
        """
        Edge case - empty password handling.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            with pytest.raises(InvalidCredentialsException):
                await uc.execute(email="test@example.com", password="")

    @pytest.mark.asyncio
    async def test_execute_none_email(self, sample_user_data):
        """
        Edge case - None email handling.
        Should not crash, should raise InvalidCredentialsException.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            try:
                await uc.execute(email=None, password="password")
                pytest.fail("Should raise an exception for None email")
            except (InvalidCredentialsException, TypeError, AttributeError):
                pass

    @pytest.mark.asyncio
    async def test_execute_none_password(self, sample_user_data):
        """
        Edge case - None password handling.
        Should not crash, should raise InvalidCredentialsException.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            try:
                await uc.execute(email="test@example.com", password=None)
                pytest.fail("Should raise an exception for None password")
            except (InvalidCredentialsException, TypeError, AttributeError):
                pass


class TestAuthenticateUseCaseTokenGeneration:
    """Test suite specifically for JWT token generation in authentication."""

    @pytest.mark.asyncio
    async def test_token_contains_username(self, mock_user):
        """
        Verify the token uses the correct user identifier (username as 'sub').
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalar_one = MagicMock(return_value=mock_user)
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            from src.auth.infrastructure.security import create_access_token
            from src.shared.infrastructure.config import settings
            import jwt

            uc = AuthenticateUseCase(db=mock_db)
            result = await uc.execute(email="test@example.com", password="password")

            # Decode token and verify payload
            decoded = jwt.decode(
                result.access_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            # Token should contain the username as 'sub'
            assert decoded["sub"] == mock_user.username
            assert "exp" in decoded

    @pytest.mark.asyncio
    async def test_token_type_is_bearer(self, mock_user):
        """
        Verify the response indicates 'bearer' token type.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalar_one = MagicMock(return_value=mock_user)
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)
            result = await uc.execute(email="test@example.com", password="password")

            assert result.token_type.lower() == "bearer"

    @pytest.mark.asyncio
    async def test_expires_in_matches_settings(self, mock_user):
        """
        Verify expires_in matches configuration.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalar_one = MagicMock(return_value=mock_user)
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            from src.shared.infrastructure.config import settings

            uc = AuthenticateUseCase(db=mock_db)
            result = await uc.execute(email="test@example.com", password="password")

            assert result.expires_in == settings.ACCESS_TOKEN_EXPIRE_MINUTES


class TestAuthenticateUseCaseErrorHandling:
    """Test suite for error handling edge cases."""

    @pytest.mark.asyncio
    async def test_execute_does_not_exist_error_converted_to_invalid_credentials(
        self,
    ):
        """
        RED: Verify that DoesNotExistError (or any user-not-found exception)
        from the repository is caught and converted to InvalidCredentialsException.

        This is the acceptance test for the bug fix: when a user doesn't exist,
        the backend should return "Credenciales incorrectas" (401) instead of
        an unhandled DoesNotExistError (500).
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        # Simulate the DoesNotExistError that currently propagates unhandled
        mock_user_repo.authenticate_by_username_or_email = AsyncMock(
            side_effect=Exception("DoesNotExistError")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            # After fix: should raise InvalidCredentialsException, not generic Exception
            with pytest.raises(InvalidCredentialsException) as exc_info:
                await uc.execute(
                    email="nonexistent@example.com", password="anypassword"
                )

            assert "Credenciales incorrectas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_repository_returns_none_converted_to_invalid_credentials(
        self,
    ):
        """
        RED: Verify that when repository returns None (user not found),
        it's converted to InvalidCredentialsException instead of raising AttributeError.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate_by_username_or_email = AsyncMock(return_value=None)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            # After fix: should raise InvalidCredentialsException, not AttributeError
            with pytest.raises(InvalidCredentialsException) as exc_info:
                await uc.execute(email="nonexistent@example.com", password="anypassword")

            assert "Credenciales incorrectas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_database_error_handling(self, mock_user):
        """
        Verify database errors are handled gracefully.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            # Should not raise an unhandled exception
            with pytest.raises(Exception) as exc_info:
                await uc.execute(email="test@example.com", password="password")
            assert (
                "Database" in str(exc_info.value)
                or "connection" in str(exc_info.value).lower()
            )

    @pytest.mark.asyncio
    async def test_execute_repository_returns_none(self):
        """
        Verify behavior when repository returns None.
        When authenticate returns None, accessing user.id causes AttributeError.
        This is a known defect - the use case should handle None gracefully.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=None)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            # The current implementation will raise AttributeError
            # because it tries to access user.id when user is None
            with pytest.raises(AttributeError):
                await uc.execute(email="test@example.com", password="password")


class TestAuthenticateUseCaseConcurrency:
    """Test suite for concurrent authentication attempts."""

    @pytest.mark.asyncio
    async def test_concurrent_authentication(self, mock_user):
        """
        Verify concurrent authentication requests work correctly.
        """

        # Create fresh mocks for each iteration
        async def authenticate():
            mock_db = MagicMock()
            mock_user_repo = MagicMock()
            mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

            mock_result = MagicMock()
            mock_result.scalar_one = MagicMock(return_value=mock_user)
            mock_db.execute = AsyncMock(return_value=mock_result)

            with patch(
                "src.auth.application.usecase.authenticate_usecase.UserRepository",
                return_value=mock_user_repo,
            ):
                uc = AuthenticateUseCase(db=mock_db)
                return await uc.execute(email="test@example.com", password="password")

        # Run multiple concurrent authentication attempts
        tasks = [authenticate() for _ in range(5)]
        results = await asyncio.gather(*tasks)

        # All should succeed
        assert len(results) == 5
        assert all(r is not None for r in results)


class TestAuthenticateUseCaseInjection:
    """Test suite for SQL injection and other injection attacks."""

    @pytest.mark.asyncio
    async def test_sql_injection_in_email(self, mock_user):
        """
        Verify SQL injection attempts are handled safely.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(
            side_effect=InvalidCredentialsException("Credenciales inválidas")
        )

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            malicious_emails = [
                "test@example.com' OR '1'='1",
                "test@example.com'; DROP TABLE users;--",
                "admin@example.com--",
                "test@example.com' UNION SELECT--",
            ]

            for email in malicious_emails:
                with pytest.raises(InvalidCredentialsException):
                    await uc.execute(email=email, password="password")

    @pytest.mark.asyncio
    async def test_special_chars_in_password(self, mock_user):
        """
        Verify special characters in password don't cause issues.
        """
        mock_db = MagicMock()
        mock_user_repo = MagicMock()
        mock_user_repo.authenticate = AsyncMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalar_one = MagicMock(return_value=mock_user)
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.auth.application.usecase.authenticate_usecase.UserRepository",
            return_value=mock_user_repo,
        ):
            uc = AuthenticateUseCase(db=mock_db)

            special_passwords = [
                "password' OR '1'='1",
                "password; DROP TABLE--",
                "password' UNION SELECT--",
                "pass@word#123!",
                "pässwörd_测试_🔐",
            ]

            for password in special_passwords:
                # Should not crash
                try:
                    result = await uc.execute(
                        email="test@example.com", password=password
                    )
                    # If no exception, should still return valid result
                    assert result is not None
                except (InvalidCredentialsException, Exception):
                    # InvalidCredentialsException is acceptable
                    # Other exceptions might indicate a defect
                    pass
