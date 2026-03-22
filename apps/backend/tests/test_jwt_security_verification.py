"""
Verification tests for JWT Bearer authentication in Swagger UI.
Tests that match the spec requirements.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_endpoint_returns_200(test_client: AsyncClient):
    """Health endpoint is public and returns 200."""
    response = await test_client.get("/health")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_auth_endpoints_accessible_without_token(test_client: AsyncClient):
    """Auth endpoints (login, register) should be accessible without token.
    They may return 422 for bad credentials, but NOT 401.
    """
    # Test login endpoint with invalid credentials (should return 422, not 401)
    response = await test_client.post(
        "/api/v1/auth/login", json={"username": "nonexistent", "password": "wrong"}
    )
    assert response.status_code != 401, f"Login returned 401, expected 422 or other"
    # Could be 404, 422, etc. We just ensure it's not 401
    # Similarly register endpoint (should not require auth)
    response = await test_client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "ValidPassword123!",
        },
    )
    assert response.status_code != 401, (
        f"Register returned 401, expected success or validation error"
    )


@pytest.mark.anyio
async def test_protected_endpoints_require_auth(test_client: AsyncClient):
    """Protected endpoints should return 401 when no token provided."""
    # List of known protected endpoints (from router structure)
    protected_endpoints = [
        ("GET", "/api/v1/users/professors/me"),
        ("GET", "/api/v1/users/students"),
        ("GET", "/api/v1/games"),
        ("GET", "/api/v1/game-instances/123/instances"),  # dummy id, should still 401
        ("GET", "/api/v1/levels/123"),
        ("POST", "/api/v1/sync/events"),  # example
    ]
    for method, path in protected_endpoints:
        response = await test_client.request(method, path)
        assert response.status_code == 401, (
            f"{method} {path} returned {response.status_code}, expected 401"
        )
        assert response.headers.get("WWW-Authenticate") == "Bearer"


@pytest.mark.anyio
async def test_invalid_token_returns_401(test_client: AsyncClient):
    """Protected endpoint with invalid token should return 401."""
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = await test_client.get("/api/v1/users/professors/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_malformed_header_returns_401(test_client: AsyncClient):
    """Malformed Authorization header should return 401."""
    # Missing Bearer prefix
    headers = {"Authorization": "invalid"}
    response = await test_client.get("/api/v1/users/professors/me", headers=headers)
    assert response.status_code == 401
    # Wrong scheme
    headers = {"Authorization": "Basic abc"}
    response = await test_client.get("/api/v1/users/professors/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_openapi_schema_has_security_schemes(test_client: AsyncClient):
    """OpenAPI schema should contain security schemes definition."""
    response = await test_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "components" in schema
    assert "securitySchemes" in schema["components"]
    schemes = schema["components"]["securitySchemes"]
    # Should have at least one HTTPBearer scheme
    bearer_schemes = [
        s
        for s in schemes.values()
        if s.get("type") == "http" and s.get("scheme") == "bearer"
    ]
    assert len(bearer_schemes) > 0, "No HTTPBearer security scheme found"
