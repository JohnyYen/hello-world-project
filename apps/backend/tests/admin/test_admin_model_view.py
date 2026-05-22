"""
Unit tests for AdminModelView authorization.

Tests authorization checks in BaseAdminModelView.
"""

import pytest
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient
from types import ModuleType

# Mock sqladmin before any imports
sqladmin_mock = ModuleType("sqladmin")
sqladmin_mock.Admin = MagicMock()
sqladmin_mock.ModelView = MagicMock()
sqladmin_mock.AdminView = MagicMock()
sys.modules["sqladmin"] = sqladmin_mock

from src.admin.admin import BaseAdminModelView, UserAdminView
from src.users.domain.user import User


class TestBaseAdminModelViewAuthorization:
    """Test suite for BaseAdminModelView authorization."""

    @pytest.mark.asyncio
    async def test_check_admin_role_returns_true_for_admin_user(
        self, mock_admin_user, admin_role
    ):
        """
        Test that _check_admin_role returns True for admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_admin_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=True)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view._check_admin_role(mock_request)

            assert result is True
            mock_verify.assert_called_once_with(mock_admin_user, mock_request.state.admin_session)

    @pytest.mark.asyncio
    async def test_check_admin_role_returns_false_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that _check_admin_role returns False for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view._check_admin_role(mock_request)

            assert result is False

    @pytest.mark.asyncio
    async def test_check_admin_role_returns_false_when_no_user(
        self,
    ):
        """
        Test that _check_admin_role returns False when no user in request.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = None
        mock_request.state.admin_session = None

        view = UserAdminView(User, MagicMock())
        view.model = User

        result = await view._check_admin_role(mock_request)

        assert result is False

    @pytest.mark.asyncio
    async def test_check_admin_role_returns_false_when_no_session(
        self, mock_admin_user
    ):
        """
        Test that _check_admin_role returns False when no session in request.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_admin_user
        mock_request.state.admin_session = None

        view = UserAdminView(User, MagicMock())
        view.model = User

        result = await view._check_admin_role(mock_request)

        assert result is False


class TestAdminModelViewListAuthorization:
    """Test suite for list method authorization."""

    @pytest.mark.asyncio
    async def test_list_returns_403_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that list returns 403 for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view.list(mock_request)

            assert result.status_code == 403
            assert "Acceso denegado" in result.body.decode()


class TestAdminModelViewDetailAuthorization:
    """Test suite for detail method authorization."""

    @pytest.mark.asyncio
    async def test_detail_returns_403_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that detail returns 403 for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view.detail(mock_request, pk="1")

            assert result.status_code == 403


class TestAdminModelViewInsertAuthorization:
    """Test suite for insert method authorization."""

    @pytest.mark.asyncio
    async def test_insert_returns_403_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that insert returns 403 for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view.insert(mock_request)

            assert result.status_code == 403


class TestAdminModelViewEditAuthorization:
    """Test suite for edit method authorization."""

    @pytest.mark.asyncio
    async def test_edit_returns_403_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that edit returns 403 for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view.edit(mock_request, pk="1")

            assert result.status_code == 403


class TestAdminModelViewDeleteAuthorization:
    """Test suite for delete method authorization."""

    @pytest.mark.asyncio
    async def test_delete_returns_403_for_non_admin_user(
        self, mock_professor_user
    ):
        """
        Test that delete returns 403 for non-admin user.
        """
        mock_request = MagicMock()
        mock_request.state.admin_user = mock_professor_user
        mock_request.state.admin_session = MagicMock()

        mock_verify = AsyncMock(return_value=False)

        with patch("src.admin.admin.verify_admin_role", mock_verify):
            view = UserAdminView(User, MagicMock())
            view.model = User

            result = await view.delete(mock_request, pk="1")

            assert result.status_code == 403