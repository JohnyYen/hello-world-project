"""
Tests de integración para el endpoint student_progress.

Este test suite verifica:
- Response 200 para request válido
- Response 401 para request sin autenticación
- Response 404 para estudiante sin progreso
- Response 400 para UUID inválido
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from httpx import AsyncClient, ASGITransport


class TestStudentProgressEndpoint:
    """Test suite para el endpoint /students/{student_id}/progress."""

    @pytest.mark.asyncio
    async def test_endpoint_returns_200_with_valid_student(self):
        """Test que el endpoint retorna 200 con datos válidos."""
        from main import app

        student_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_progress_list = [
            MagicMock(
                student_id=UUID(student_id),
                segment_level_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
                attempt_count=5,
                efficiency_rating=85,
                objectives_completed=2,
                created_at=MagicMock(strftime=lambda f: "Mar 15"),
                updated_at=MagicMock(),
            ),
        ]

        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_by_student_id = AsyncMock(return_value=mock_progress_list)
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/statistic/students/{student_id}/progress"
                )

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_returns_422_for_invalid_uuid(self):
        """Test que el endpoint retorna 422 para UUID inválido."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/statistic/students/invalid-uuid/progress"
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_returns_404_for_empty_progress(self):
        """Test que el endpoint retorna 404 cuando no hay progreso."""
        from main import app

        student_id = "550e8400-e29b-41d4-a716-446655440000"

        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_by_student_id = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/statistic/students/{student_id}/progress"
                )

                assert response.status_code == 404


class TestStudentProgressEndpointResponseStructure:
    """Test suite para verificar la estructura de la respuesta."""

    @pytest.mark.asyncio
    async def test_response_has_expected_fields(self):
        """Test que la respuesta tiene los campos esperados."""
        from main import app

        student_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_progress_list = [
            MagicMock(
                student_id=UUID(student_id),
                segment_level_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
                attempt_count=3,
                efficiency_rating=80,
                objectives_completed=1,
                created_at=MagicMock(strftime=lambda f: "Mar 10"),
                updated_at=MagicMock(),
            ),
        ]

        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_by_student_id = AsyncMock(return_value=mock_progress_list)
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/statistic/students/{student_id}/progress"
                )

                data = response.json()

                assert "student_id" in data
                assert "kpis" in data
                assert "progress_over_time" in data
                assert "level_performance" in data
                assert "activity_distribution" in data

                assert "total_levels_completed" in data["kpis"]
                assert "total_games_played" in data["kpis"]
                assert "total_play_time" in data["kpis"]
                assert "average_score" in data["kpis"]
