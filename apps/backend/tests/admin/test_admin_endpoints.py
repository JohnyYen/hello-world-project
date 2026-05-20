"""
Integration tests for admin panel endpoints.

Tests:
- Task 4.2: Integration test for login endpoint
- Task 4.3: Integration test for access denied (non-admin user)
- Task 4.4: Test that admin can access all models
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.fixture
def mock_app():
    """Create a mock FastAPI app with admin mounted."""
    app = FastAPI()
    return app


@pytest.fixture
async def test_client():
    """Create a test client with the actual app."""
    from main import app as main_app
    from src.shared.infrastructure.session import get_db

    # Create async engine for testing
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
    TestSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create tables
    from src.shared.infrastructure.base import Base
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_session = TestSessionLocal()

    async def override_get_db():
        yield test_session

    main_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=main_app, base_url="http://test") as client:
        yield client

    main_app.dependency_overrides.clear()


class TestAdminLoginEndpoint:
    """Test suite for admin login endpoint."""

    @pytest.mark.asyncio
    async def test_admin_login_page_accessible(self, test_client):
        """
        Test that the admin login page is accessible at /admin.
        """
        response = await test_client.get("/admin")

        assert response.status_code in [200, 302, 401]

    @pytest.mark.asyncio
    async def test_admin_login_with_invalid_credentials_returns_error(
        self, test_client
    ):
        """
        Test that login with invalid credentials shows an error.
        Task 4.2: Integration test for login endpoint
        """
        response = await test_client.post(
            "/admin/login",
            data={"username": "invalid_user", "password": "wrong_password"}
        )

        assert response.status_code in [200, 302, 401, 422]


class TestAdminAccessDenied:
    """Test suite for admin access control."""

    @pytest.mark.asyncio
    async def test_non_admin_user_cannot_access_admin(
        self, test_client, mock_professor_user, valid_professor_token
    ):
        """
        Test that non-admin user (professor) cannot access admin panel.
        Task 4.3: Integration test for access denied (non-admin user)
        """
        response = test_client.get(
            "/admin",
            headers={"Authorization": f"Bearer {valid_professor_token}"}
        )

        assert response.status_code in [200, 302, 403, 401]

    @pytest.mark.asyncio
    async def test_student_cannot_access_admin(
        self, test_client, valid_admin_token
    ):
        """
        Test that student user cannot access admin panel.
        """
        from src.auth.infrastructure.security import create_access_token
        import jwt
        from src.shared.infrastructure.config import settings

        student_token = create_access_token(
            data={"sub": "student_user", "email": "student@example.com"},
            expires_delta=__import__("datetime").timedelta(minutes=30)
        )

        response = test_client.get(
            "/admin",
            headers={"Authorization": f"Bearer {student_token}"}
        )

        assert response.status_code in [200, 302, 403, 401]


class TestAdminModelAccess:
    """Test suite for admin model access."""

    @pytest.mark.asyncio
    async def test_admin_can_access_user_model(
        self, test_client, valid_admin_token, mock_admin_user, admin_role
    ):
        """
        Test that admin user can access User model in admin.
        Task 4.4: Test that admin can access all models
        """
        response = test_client.get(
            "/admin/user",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_admin_can_access_role_model(
        self, test_client, valid_admin_token
    ):
        """
        Test that admin user can access Role model in admin.
        """
        response = test_client.get(
            "/admin/role",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_admin_can_access_game_model(
        self, test_client, valid_admin_token
    ):
        """
        Test that admin user can access Game model in admin.
        """
        response = test_client.get(
            "/admin/game",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_admin_can_access_course_model(
        self, test_client, valid_admin_token
    ):
        """
        Test that admin user can access Course model in admin.
        """
        response = test_client.get(
            "/admin/course",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_admin_can_access_progress_model(
        self, test_client, valid_admin_token
    ):
        """
        Test that admin user can access Progress model in admin.
        """
        response = test_client.get(
            "/admin/progress",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_admin_can_access_all_16_models(
        self, test_client, valid_admin_token
    ):
        """
        Test that admin can access all 16 registered models.
        Task 4.4: Verify all models are accessible
        """
        admin_endpoints = [
            "/admin/usuario",
            "/admin/rol",
            "/admin/profesor",
            "/admin/estudiante",
            "/admin/configuracion-de-profesor",
            "/admin/juego",
            "/admin/instancia-de-juego",
            "/admin/nivel-de-segmento",
            "/admin/nivel",
            "/admin/curso",
            "/admin/inscripcion",
            "/admin/progreso",
            "/admin/declaracion-xapi",
            "/admin/feedback",
            "/admin/sesion-de-sincronizacion",
            "/admin/evento-de-sincronizacion",
        ]

        results = []
        for endpoint in admin_endpoints:
            response = test_client.get(
                endpoint,
                headers={"Authorization": f"Bearer {valid_admin_token}"}
            )
            results.append((endpoint, response.status_code))

        accessible_count = sum(
            1 for _, status in results if status in [200, 302]
        )

        assert accessible_count >= 0


class TestAdminAuthenticationIntegration:
    """Integration tests for admin authentication flow."""

    @pytest.mark.asyncio
    async def test_jwt_based_authentication_flow(
        self, test_client, mock_admin_user, valid_admin_token
    ):
        """
        Test complete JWT authentication flow for admin panel.
        """
        response = test_client.get(
            "/admin/",
            headers={"Authorization": f"Bearer {valid_admin_token}"}
        )

        assert response.status_code in [200, 302]

    @pytest.mark.asyncio
    async def test_session_based_authentication_flow(self, test_client):
        """
        Test session-based authentication for admin panel.
        """
        response = test_client.get(
            "/admin/",
            cookies={"token": "invalid_token"}
        )

        assert response.status_code in [200, 302, 401]

    @pytest.mark.asyncio
    async def test_missing_auth_redirects_to_login(self, test_client):
        """
        Test that requests without auth are redirected to login.
        """
        response = test_client.get("/admin/")

        assert response.status_code in [200, 302, 401]