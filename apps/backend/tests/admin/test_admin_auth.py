"""
Unit tests for AdminAuth and verify_admin_role functions.

Tests:
- Task 4.1: Unit tests for authentication methods (verify_admin_role, authenticate)
"""

import pytest
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from types import ModuleType

# Mock sqladmin before any imports
sqladmin_mock = ModuleType("sqladmin")
sqladmin_mock.Admin = MagicMock()
sqladmin_mock.ModelView = MagicMock()
sqladmin_mock.AdminView = MagicMock()
sys.modules["sqladmin"] = sqladmin_mock

from src.admin.auth import (
    AdminAuth,
    verify_admin_role,
    admin_auth,
    AdminUser,
)


class TestVerifyAdminRole:
    """Test suite for verify_admin_role function."""

    @pytest.mark.asyncio
    async def test_verify_admin_role_with_admin_user_returns_true(
        self, mock_admin_user, admin_role, admin_test_session
    ):
        """
        Test that verify_admin_role returns True for admin user.
        """
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = admin_role
        admin_test_session.execute = AsyncMock(return_value=mock_result)

        result = await verify_admin_role(mock_admin_user, admin_test_session)

        assert result is True
        admin_test_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_admin_role_with_professor_returns_false(
        self, mock_professor_user, professor_role, admin_test_session
    ):
        """
        Test that verify_admin_role returns False for professor user.
        """
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = professor_role
        admin_test_session.execute = AsyncMock(return_value=mock_result)

        result = await verify_admin_role(mock_professor_user, admin_test_session)

        assert result is False

    @pytest.mark.asyncio
    async def test_verify_admin_role_with_student_returns_false(
        self, mock_student_user, student_role, admin_test_session
    ):
        """
        Test that verify_admin_role returns False for student user.
        """
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = student_role
        admin_test_session.execute = AsyncMock(return_value=mock_result)

        result = await verify_admin_role(mock_student_user, admin_test_session)

        assert result is False

    @pytest.mark.asyncio
    async def test_verify_admin_role_with_no_role_returns_false(
        self, mock_admin_user, admin_test_session
    ):
        """
        Test that verify_admin_role returns False when user has no role.
        """
        mock_admin_user.role_id = None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        admin_test_session.execute = AsyncMock(return_value=mock_result)

        result = await verify_admin_role(mock_admin_user, admin_test_session)

        assert result is False

    @pytest.mark.asyncio
    async def test_verify_admin_role_when_role_not_found(
        self, mock_admin_user, admin_test_session
    ):
        """
        Test that verify_admin_role returns False when role is not found.
        """
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        admin_test_session.execute = AsyncMock(return_value=mock_result)

        result = await verify_admin_role(mock_admin_user, admin_test_session)

        assert result is False


class TestAdminAuthAuthenticate:
    """Test suite for AdminAuth.authenticate method."""

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_credentials_returns_user(
        self, mock_admin_user, admin_test_session
    ):
        """
        Test successful authentication with valid username and password.
        """
        admin_auth_instance = AdminAuth()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_admin_user

        with patch.object(
            admin_test_session, "execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value = mock_user_result

            result = await admin_auth_instance.authenticate(
                username="admin_user",
                password="AdminPass123!",
                session=admin_test_session
            )

            assert result is not None
            assert result.id == mock_admin_user.id
            assert result.username == mock_admin_user.username

    @pytest.mark.asyncio
    async def test_authenticate_with_invalid_password_returns_none(
        self, mock_admin_user, admin_test_session
    ):
        """
        Test authentication fails with wrong password.
        """
        admin_auth_instance = AdminAuth()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_admin_user

        with patch.object(
            admin_test_session, "execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value = mock_user_result

            result = await admin_auth_instance.authenticate(
                username="admin_user",
                password="WrongPassword",
                session=admin_test_session
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_with_nonexistent_user_returns_none(
        self, admin_test_session
    ):
        """
        Test authentication fails when user doesn't exist.
        """
        admin_auth_instance = AdminAuth()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = None

        with patch.object(
            admin_test_session, "execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value = mock_user_result

            result = await admin_auth_instance.authenticate(
                username="nonexistent_user",
                password="any_password",
                session=admin_test_session
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_with_inactive_user_returns_none(
        self, mock_inactive_admin_user, admin_test_session
    ):
        """
        Test authentication fails for inactive user.
        """
        admin_auth_instance = AdminAuth()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_inactive_admin_user

        with patch.object(
            admin_test_session, "execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value = mock_user_result

            result = await admin_auth_instance.authenticate(
                username="inactive_admin",
                password="AdminPass123!",
                session=admin_test_session
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_with_email_as_username(
        self, mock_admin_user, admin_test_session
    ):
        """
        Test authentication works when using email as username.
        """
        admin_auth_instance = AdminAuth()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_admin_user

        with patch.object(
            admin_test_session, "execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value = mock_user_result

            result = await admin_auth_instance.authenticate(
                username="admin@example.com",
                password="AdminPass123!",
                session=admin_test_session
            )

            assert result is not None
            assert result.email == mock_admin_user.email


class TestAdminAuthVerifyToken:
    """Test suite for AdminAuth.verify_token method."""

    @pytest.mark.asyncio
    async def test_verify_token_with_expired_token_returns_none(
        self, expired_token
    ):
        """
        Test that verify_token returns None for expired token.
        """
        admin_auth_instance = AdminAuth()

        mock_request = MagicMock()
        mock_request.session = {}
        mock_request.headers = {"authorization": f"Bearer {expired_token}"}

        result = await admin_auth_instance.verify_token(mock_request)

        assert result is None

    @pytest.mark.asyncio
    async def test_verify_token_with_no_token_returns_none(self):
        """
        Test that verify_token returns None when no token is provided.
        """
        admin_auth_instance = AdminAuth()

        mock_request = MagicMock()
        mock_request.session = {}
        mock_request.headers = {}

        result = await admin_auth_instance.verify_token(mock_request)

        assert result is None

    @pytest.mark.asyncio
    async def test_verify_token_with_invalid_token_returns_none(self):
        """
        Test that verify_token returns None for invalid token.
        """
        admin_auth_instance = AdminAuth()

        mock_request = MagicMock()
        mock_request.session = {}
        mock_request.headers = {"authorization": "Bearer invalid.token.here"}

        result = await admin_auth_instance.verify_token(mock_request)

        assert result is None


class TestAdminUserWrapper:
    """Test suite for AdminUser wrapper class."""

    def test_admin_user_wrapper_creates_correctly(self, mock_admin_user):
        """
        Test AdminUser wrapper correctly wraps User object.
        """
        admin_user = AdminUser(mock_admin_user)

        assert admin_user.id == mock_admin_user.id
        assert admin_user.username == mock_admin_user.username
        assert admin_user.email == mock_admin_user.email
        assert admin_user.is_active == mock_admin_user.is_active

    def test_admin_user_is_authenticated_returns_active_status(
        self, mock_admin_user
    ):
        """
        Test is_authenticated property returns correct value.
        """
        admin_user = AdminUser(mock_admin_user)

        assert admin_user.is_authenticated is True

    def test_admin_user_is_authenticated_returns_false_for_inactive(
        self, mock_inactive_admin_user
    ):
        """
        Test is_authenticated returns False for inactive user.
        """
        admin_user = AdminUser(mock_inactive_admin_user)

        assert admin_user.is_authenticated is False