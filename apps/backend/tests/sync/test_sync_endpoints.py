"""
Integration tests for Sync API endpoints.

This test suite verifies:
- start_session endpoint
- register_event endpoint
- Event creation with invalid session_id validation
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from httpx import AsyncClient, ASGITransport


class TestStartSessionEndpoint:
    """Test suite for start_sync_session endpoint."""

    @pytest.mark.asyncio
    async def test_start_session_success(self, mock_sync_session):
        """Test successful session start via endpoint."""
        with patch("src.sync.api.v1.dependencies.get_sync_session_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(return_value=mock_sync_session)
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.start_sync_session import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_instance_id = str(uuid.uuid4())

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-sessions", json={"instance_id": test_instance_id})

            assert response.status_code == 201
            data = response.json()
            assert "id" in data

    @pytest.mark.asyncio
    async def test_start_session_returns_201(self):
        """Test that endpoint returns 201 Created on success."""
        mock_session = MagicMock()
        mock_session.id = uuid.uuid4()
        mock_session.instance_id = uuid.uuid4()
        mock_session.status = "active"
        mock_session.start_time = datetime.now(timezone.utc)
        mock_session.end_time = None

        with patch("src.sync.api.v1.dependencies.get_sync_session_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(return_value=mock_session)
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.start_sync_session import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_instance_id = str(uuid.uuid4())

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-sessions", json={"instance_id": test_instance_id})

            assert response.status_code == 201


class TestRegisterEventEndpoint:
    """Test suite for register_sync_event endpoint."""

    @pytest.mark.asyncio
    async def test_register_event_success(self, mock_sync_event):
        """Test successful event registration via endpoint."""
        with patch("src.sync.api.v1.dependencies.get_sync_event_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(return_value=mock_sync_event)
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.register_sync_event import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_session_id = str(uuid.uuid4())

            event_payload = {
                "sync_session_id": test_session_id,
                "event_type": "player_action",
                "payload": {"action": "move"},
            }

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-events", json=event_payload)

            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert data["event_type"] == "player_action"

    @pytest.mark.asyncio
    async def test_register_event_returns_201(self):
        """Test that endpoint returns 201 Created on success."""
        mock_event = MagicMock()
        mock_event.id = uuid.uuid4()
        mock_event.sync_session_id = uuid.uuid4()
        mock_event.event_type = "player_action"
        mock_event.payload = {"action": "move"}
        mock_event.timestamp = datetime.now(timezone.utc)
        mock_event.status = "pending"

        with patch("src.sync.api.v1.dependencies.get_sync_event_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(return_value=mock_event)
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.register_sync_event import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_session_id = str(uuid.uuid4())

            event_payload = {
                "sync_session_id": test_session_id,
                "event_type": "player_action",
                "payload": {"action": "move"},
            }

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-events", json=event_payload)

            assert response.status_code == 201


class TestEventValidationSessionNotExists:
    """Test suite for event validation - session doesn't exist."""

    @pytest.mark.asyncio
    async def test_register_event_invalid_session_returns_404(self):
        """Test that creating event with invalid session_id returns 404."""
        from src.shared.domain.exceptions import NotFoundException

        with patch("src.sync.api.v1.dependencies.get_sync_event_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(
                side_effect=NotFoundException(
                    f"Sesión de sincronización {uuid.uuid4()} no encontrada"
                )
            )
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.register_sync_event import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_session_id = str(uuid.uuid4())

            event_payload = {
                "sync_session_id": test_session_id,
                "event_type": "player_action",
                "payload": {"action": "move"},
            }

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-events", json=event_payload)

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_register_event_error_message_in_response(self):
        """Test that error message is included in 404 response."""
        error_message = f"Sesión de sincronización {uuid.uuid4()} no encontrada"

        with patch("src.sync.api.v1.dependencies.get_sync_event_service") as mock_dep:
            mock_service = MagicMock()
            mock_service.create = AsyncMock(
                side_effect=NotFoundException(error_message)
            )
            mock_dep.return_value = mock_service

            from src.sync.api.v1.endpoints.register_sync_event import router
            from fastapi import FastAPI

            app = FastAPI()
            app.include_router(router)

            test_session_id = str(uuid.uuid4())

            event_payload = {
                "sync_session_id": test_session_id,
                "event_type": "player_action",
                "payload": {"action": "move"},
            }

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post("/sync-events", json=event_payload)

            assert response.status_code == 404
            assert error_message in response.json()["detail"]
