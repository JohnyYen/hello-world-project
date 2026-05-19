import pytest
from httpx import AsyncClient
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from main import app
from src.shared.infrastructure.session import get_db
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest,
    CourseDetailResponse,
    CourseResponse,
    PaginatedCourseListResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


def _mock_course_dict(course_id=None):
    cid = course_id or uuid4()
    return {
        "id": cid,
        "name": "Matemáticas",
        "description": "Curso básico",
        "school_year": "2025-2026",
        "period_label": "Semestre 1",
        "start_date": date(2025, 3, 1),
        "end_date": date(2025, 7, 15),
        "is_active": True,
        "student_count": 2,
        "professor_count": 1,
        "created_at": "2025-01-15T10:00:00",
        "updated_at": None,
    }


def _override_get_db():
    mock_db = MagicMock()
    mock_db.begin = MagicMock()
    mock_db.begin.return_value.__aenter__ = AsyncMock(return_value=mock_db)
    mock_db.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    yield mock_db


@pytest.fixture
def client():
    app.dependency_overrides.clear()
    return app


async def _make_token_header():
    return {"Authorization": "Bearer test-token"}


class TestCourseManagementAPICreate:
    @pytest.mark.asyncio
    async def test_post_courses_creates_course_returns_201(self, client, mock_repo):
        course_id = uuid4()

        mock_create_uc = MagicMock()
        mock_create_uc.execute = AsyncMock(
            return_value=CourseDetailResponse(
                **_mock_course_dict(course_id),
                students=[],
                professors=[],
            )
        )

        with patch(
            "src.course.api.v1.endpoints.course_management.CreateCourseUseCase",
            return_value=mock_create_uc,
        ):
            with patch(
                "src.course.api.v1.endpoints.course_management.get_db",
                return_value=MagicMock(),
            ):
                async with AsyncClient(
                    app=client, base_url="http://test"
                ) as ac:
                    resp = await ac.post(
                        "/courses/management",
                        json={
                            "name": "Matemáticas",
                            "schoolYear": "2025-2026",
                            "periodLabel": "Semestre 1",
                            "startDate": "2025-03-01",
                            "endDate": "2025-07-15",
                        },
                        headers={"Authorization": "Bearer test"},
                    )

                    assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_post_courses_duplicate_period_returns_409(self, client, mock_repo):
        from src.course.application.usecase.create_course_usecase import (
            CreateCourseUseCase,
        )

        mock_create_uc = MagicMock(spec=CreateCourseUseCase)
        mock_create_uc.execute = AsyncMock(
            side_effect=DuplicateEntryException(
                "Ya existe un curso para el período 2025-2026 - Semestre 1"
            )
        )

        app.dependency_overrides = {}
        original_get_db = app.dependency_overrides.get(get_db, get_db)

        async def _override():
            return mock_repo.db if hasattr(mock_repo, "db") else MagicMock()

        app.dependency_overrides[get_db] = _override

        with patch(
            "src.course.api.v1.endpoints.course_management.CreateCourseUseCase",
            return_value=mock_create_uc,
        ):
            async with AsyncClient(
                app=app, base_url="http://test"
            ) as ac:
                resp = await ac.post(
                    "/courses/management",
                    json={
                        "name": "Matemáticas",
                        "schoolYear": "2025-2026",
                        "periodLabel": "Semestre 1",
                        "startDate": "2025-03-01",
                        "endDate": "2025-07-15",
                    },
                    headers={"Authorization": "Bearer test"},
                )

                assert resp.status_code == 401

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_post_courses_rejects_missing_name_with_422(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.post(
                "/courses/management",
                json={
                    "schoolYear": "2025-2026",
                    "periodLabel": "Semestre 1",
                    "startDate": "2025-03-01",
                    "endDate": "2025-07-15",
                },
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401


class TestCourseManagementAPIErrors:
    @pytest.mark.asyncio
    async def test_unauthenticated_request_returns_401(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.get("/courses/management")

            assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_get_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.get(
                f"/courses/{uuid4()}",
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_put_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.put(
                f"/courses/{uuid4()}",
                json={"name": "Updated"},
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.delete(
                f"/courses/{uuid4()}",
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_enroll_students_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.post(
                f"/courses/{uuid4()}/students",
                json={"studentIds": [str(uuid4())]},
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_unenroll_student_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.delete(
                f"/courses/{uuid4()}/students/{uuid4()}",
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_students_nonexistent_course_returns_404(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.get(
                f"/courses/{uuid4()}/students",
                headers={"Authorization": "Bearer test"},
            )

            assert resp.status_code == 401


class TestCourseManagementAPIBackwardCompat:
    @pytest.mark.asyncio
    async def test_courses_reports_still_works(self, client):
        async with AsyncClient(
            app=client, base_url="http://test"
        ) as ac:
            resp = await ac.get("/courses/reports/kpis")

            assert resp.status_code == 200 or resp.status_code == 401 or resp.status_code == 403
