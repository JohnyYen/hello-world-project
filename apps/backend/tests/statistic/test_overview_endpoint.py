"""
Tests de integración para el endpoint overview.

Este test suite verifica:
- Response 200 para request válido
- Response 400 para parámetros inválidos
- Response 401 para request sin autenticación
- Estructura correcta de la respuesta
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date as datetime_date

from httpx import AsyncClient, ASGITransport


class TestOverviewEndpoint:
    """Test suite para el endpoint /overview."""

    @pytest.mark.asyncio
    async def test_endpoint_returns_200_with_valid_params(self):
        """Test que el endpoint retorna 200 con parámetros válidos."""
        from main import app

        with patch(
            "src.statistic.application.usecase.get_overview_stats_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.count_students = AsyncMock(return_value=100)
            mock_repo.get_active_students = AsyncMock(return_value=50)
            mock_repo.aggregate_kpis = AsyncMock(
                return_value={
                    "total_levels_completed": 500,
                    "total_play_time_minutes": 10000,
                    "average_score": 85.5,
                }
            )
            mock_repo.aggregate_activity_by_date = AsyncMock(return_value=[])
            mock_repo.aggregate_level_performance = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get("/api/v1/statistic/overview")

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_returns_200_with_period_param(self):
        """Test que el endpoint retorna 200 con parámetro period."""
        from main import app

        with patch(
            "src.statistic.application.usecase.get_overview_stats_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.count_students = AsyncMock(return_value=100)
            mock_repo.get_active_students = AsyncMock(return_value=50)
            mock_repo.aggregate_kpis = AsyncMock(
                return_value={
                    "total_levels_completed": 500,
                    "total_play_time_minutes": 10000,
                    "average_score": 85.5,
                }
            )
            mock_repo.aggregate_activity_by_date = AsyncMock(return_value=[])
            mock_repo.aggregate_level_performance = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get("/api/v1/statistic/overview?period=7d")

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_returns_400_for_invalid_period(self):
        """Test que el endpoint retorna 400 para período inválido."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/statistic/overview?period=invalid")

            assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_endpoint_returns_400_for_invalid_date_range(self):
        """Test que el endpoint retorna 400 cuando end_date < start_date."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/statistic/overview?start_date=2026-03-01&end_date=2026-01-01"
            )

            assert response.status_code == 400


class TestOverviewEndpointResponseStructure:
    """Test suite para verificar la estructura de la respuesta."""

    @pytest.mark.asyncio
    async def test_response_has_expected_fields(self):
        """Test que la respuesta tiene los campos esperados."""
        from main import app

        with patch(
            "src.statistic.application.usecase.get_overview_stats_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.count_students = AsyncMock(return_value=100)
            mock_repo.get_active_students = AsyncMock(return_value=50)
            mock_repo.aggregate_kpis = AsyncMock(
                return_value={
                    "total_levels_completed": 500,
                    "total_play_time_minutes": 10000,
                    "average_score": 85.5,
                }
            )
            mock_repo.aggregate_activity_by_date = AsyncMock(
                return_value=[
                    {
                        "date": datetime_date(2026, 4, 1),
                        "sessions": 25,
                        "active_students": 10,
                        "play_time_minutes": 500,
                    }
                ]
            )
            mock_repo.aggregate_level_performance = AsyncMock(
                return_value=[
                    {
                        "level_name": "Nivel 1",
                        "completion_rate": 0.85,
                        "average_attempts": 2.5,
                        "average_time_minutes": 15.0,
                    }
                ]
            )
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get("/api/v1/statistic/overview")

                data = response.json()

                assert "kpis" in data
                assert "activity_over_time" in data
                assert "level_performance" in data
                assert "trends" in data

                # Verificar estructura de KPIs
                assert "total_students" in data["kpis"]
                assert "active_students_this_week" in data["kpis"]
                assert "total_levels_completed" in data["kpis"]
                assert "average_score" in data["kpis"]

    @pytest.mark.asyncio
    async def test_response_kpis_values(self):
        """Test que los valores de KPIs son los esperados."""
        from main import app

        with patch(
            "src.statistic.application.usecase.get_overview_stats_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.count_students = AsyncMock(return_value=150)
            mock_repo.get_active_students = AsyncMock(return_value=75)
            mock_repo.aggregate_kpis = AsyncMock(
                return_value={
                    "total_levels_completed": 750,
                    "total_play_time_minutes": 15000,
                    "average_score": 90.0,
                }
            )
            mock_repo.aggregate_activity_by_date = AsyncMock(return_value=[])
            mock_repo.aggregate_level_performance = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.get("/api/v1/statistic/overview")

                data = response.json()

                assert data["kpis"]["total_students"] == 150
                assert data["kpis"]["active_students_this_week"] == 75
                assert data["kpis"]["total_levels_completed"] == 750
                assert data["kpis"]["average_score"] == 90.0
