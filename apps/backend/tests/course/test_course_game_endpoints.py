"""
Integration tests: course-game endpoints (available-games + assigned-game)

Uses in-memory SQLite (from conftest.py). Verifies HTTP-layer behavior of the
new endpoints registered in course_game.py.
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4

from main import app


class TestCourseGameEndpoints:
    """HTTP-layer tests for course game endpoints."""

    @pytest.mark.asyncio
    async def test_get_available_games_returns_list(
        self, test_client: AsyncClient
    ):
        """GET /courses/available-games devuelve la lista de juegos disponibles."""
        resp = await test_client.get("/api/v1/courses/available-games")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "data" in data

    @pytest.mark.asyncio
    async def test_get_assigned_game_none_sem_course_sem_jogo(
        self, test_client: AsyncClient
    ):
        """GET /courses/{course_id}/game sin juego asignado → 204 No Content."""
        random_id = uuid4()
        resp = await test_client.get(f"/api/v1/courses/{random_id}/game")
        # 204 si no hay juego; 404 si no hay curso
        assert resp.status_code in (204, 404)

    @pytest.mark.asyncio
    async def test_available_games_requires_auth(
        self, test_client: AsyncClient
    ):
        """Sin token JWT, devuelve 401."""
        # Remove auth from client for the duration of this call
        resp = await test_client.get(
            "/api/v1/courses/available-games",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert resp.status_code == 401
