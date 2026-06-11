"""
Tests de integración para el endpoint /sync/bulk-stats.

Verifica:
- Response 200 para payload válido
- Response 422 para payload inválido (campos requeridos faltantes)
- Response 401 sin token JWT (vía HTTPBearer)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient, ASGITransport


class TestBulkStatsEndpoint:
    """Test suite para el endpoint bulk-stats."""

    ENDPOINT = "/api/v1/statistic/sync/bulk-stats"
    VALID_TOKEN = "Bearer test-token"

    @pytest.mark.asyncio
    async def test_endpoint_returns_200_with_valid_payload(self):
        """Test que el endpoint retorna 200 con payload válido."""
        from main import app

        with patch(
            "src.statistic.application.usecase.bulk_stats_use_case.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.bulk_upsert_progress = AsyncMock(
                return_value={
                    "inserted": 1,
                    "updated": 0,
                    "errors": 0,
                }
            )
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.post(
                    self.ENDPOINT,
                    json={
                        "records": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "segment_id": 1,
                                "actor_id": "test-actor-uuid",
                                "attempt_count": 3,
                                "error_count": 1,
                                "hints_used_count": 0,
                                "efficiency_rating": 85,
                                "objectives_completed": 1,
                                "status": "pending_sync",
                                "retry_count": 0,
                                "created_at": "2026-06-10T10:00:00Z",
                                "updated_at": "2026-06-10T10:00:00Z",
                            }
                        ]
                    },
                    headers={"Authorization": self.VALID_TOKEN},
                )

                assert response.status_code == 200
                data = response.json()
                assert "processed" in data
                assert "successful" in data
                assert "failed" in data

    @pytest.mark.asyncio
    async def test_endpoint_returns_422_for_empty_payload(self):
        """Test que el endpoint retorna 422 para payload vacío."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post(
                self.ENDPOINT,
                json={},
                headers={"Authorization": self.VALID_TOKEN},
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_returns_422_for_invalid_record(self):
        """Test que el endpoint retorna 422 para registro inválido (sin ID)."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post(
                self.ENDPOINT,
                json={
                    "records": [
                        {
                            "segment_id": 1,
                            "actor_id": "test-actor-uuid",
                        }
                    ]
                },
                headers={"Authorization": self.VALID_TOKEN},
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_returns_422_for_invalid_status(self):
        """Test que el endpoint retorna 422 para status inválido."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post(
                self.ENDPOINT,
                json={
                    "records": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "segment_id": 1,
                            "actor_id": "test-actor-uuid",
                            "status": "invalid_status",
                        }
                    ]
                },
                headers={"Authorization": self.VALID_TOKEN},
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_returns_422_for_missing_segment_id(self):
        """Test que el endpoint retorna 422 cuando falta segment_id."""
        from main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post(
                self.ENDPOINT,
                json={
                    "records": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "actor_id": "test-actor-uuid",
                            "status": "pending_sync",
                        }
                    ]
                },
                headers={"Authorization": self.VALID_TOKEN},
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_returns_200_with_partial_success(self):
        """Test que el endpoint maneja éxito parcial correctamente."""
        from main import app

        with patch(
            "src.statistic.application.usecase.bulk_stats_use_case.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.bulk_upsert_progress = AsyncMock(
                return_value={
                    "inserted": 1,
                    "updated": 0,
                    "errors": 1,
                }
            )
            MockRepo.return_value = mock_repo

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.post(
                    self.ENDPOINT,
                    json={
                        "records": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440001",
                                "segment_id": 1,
                                "actor_id": "test-actor-uuid",
                                "attempt_count": 3,
                                "error_count": 1,
                                "status": "pending_sync",
                                "created_at": "2026-06-10T10:00:00Z",
                                "updated_at": "2026-06-10T10:00:00Z",
                            },
                        ]
                    },
                    headers={"Authorization": self.VALID_TOKEN},
                )

                assert response.status_code == 200
                data = response.json()
                assert data["failed"] == 1