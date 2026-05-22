import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.users.application.usecase.list_users_by_role_usecase import (
    ListUsersByRoleUseCase,
)
from src.users.api.v1.schemas.user import UserListResponse, UserResponse
from src.shared.domain.exceptions import NotFoundException


class TestListUsersByRoleUseCase:
    @pytest.mark.asyncio
    async def test_execute_role_student_returns_only_students(self, mock_db):
        mock_role = MagicMock()
        mock_role.id = uuid4()

        mock_role_repo = MagicMock()
        mock_role_repo.get_by_name = AsyncMock(return_value=mock_role)

        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.username = "student1"
        mock_user.email = "student1@test.com"
        mock_user.name = "Student"
        mock_user.lastname = "One"
        mock_user.is_active = True
        mock_user.role = MagicMock()
        mock_user.role.role_name = "student"

        mock_result = MagicMock()
        mock_result.scalars.return_value.all = MagicMock(return_value=[mock_user])
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.users.application.usecase.list_users_by_role_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = ListUsersByRoleUseCase(db=mock_db)
            result = await uc.execute(role="student")

            assert isinstance(result, UserListResponse)
            assert len(result.data) == 1
            assert result.data[0].username == "student1"

    @pytest.mark.asyncio
    async def test_execute_role_professor_returns_only_professors(self, mock_db):
        mock_role = MagicMock()
        mock_role.id = uuid4()

        mock_role_repo = MagicMock()
        mock_role_repo.get_by_name = AsyncMock(return_value=mock_role)

        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.username = "prof1"
        mock_user.email = "prof1@test.com"
        mock_user.name = "Professor"
        mock_user.lastname = "One"
        mock_user.is_active = True
        mock_user.role = MagicMock()
        mock_user.role.role_name = "professor"

        mock_result = MagicMock()
        mock_result.scalars.return_value.all = MagicMock(return_value=[mock_user])
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.users.application.usecase.list_users_by_role_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = ListUsersByRoleUseCase(db=mock_db)
            result = await uc.execute(role="professor")

            assert isinstance(result, UserListResponse)
            assert len(result.data) == 1
            assert result.data[0].username == "prof1"

    @pytest.mark.asyncio
    async def test_execute_role_not_found_raises_exception(self, mock_db):
        mock_role_repo = MagicMock()
        mock_role_repo.get_by_name = AsyncMock(return_value=None)

        with patch(
            "src.users.application.usecase.list_users_by_role_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = ListUsersByRoleUseCase(db=mock_db)

            with pytest.raises(NotFoundException):
                await uc.execute(role="nonexistent")

    @pytest.mark.asyncio
    async def test_execute_no_users_for_role_returns_empty_list(self, mock_db):
        mock_role = MagicMock()
        mock_role.id = uuid4()

        mock_role_repo = MagicMock()
        mock_role_repo.get_by_name = AsyncMock(return_value=mock_role)

        mock_result = MagicMock()
        mock_result.scalars.return_value.all = MagicMock(return_value=[])
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.users.application.usecase.list_users_by_role_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = ListUsersByRoleUseCase(db=mock_db)
            result = await uc.execute(role="student")

            assert isinstance(result, UserListResponse)
            assert len(result.data) == 0

    @pytest.mark.asyncio
    async def test_execute_respects_pagination(self, mock_db):
        mock_role = MagicMock()
        mock_role.id = uuid4()

        mock_role_repo = MagicMock()
        mock_role_repo.get_by_name = AsyncMock(return_value=mock_role)

        mock_result = MagicMock()
        mock_result.scalars.return_value.all = MagicMock(
            return_value=[MagicMock() for _ in range(5)]
        )
        mock_db.execute = AsyncMock(return_value=mock_result)

        with patch(
            "src.users.application.usecase.list_users_by_role_usecase.RoleRepository",
            return_value=mock_role_repo,
        ):
            uc = ListUsersByRoleUseCase(db=mock_db)
            result = await uc.execute(role="student", skip=0, limit=5)

            assert len(result.data) == 5
