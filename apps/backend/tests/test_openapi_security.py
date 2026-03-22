"""
Tests for OpenAPI security scheme configuration.
Verifies JWT Bearer security is properly defined in OpenAPI schema.
"""

import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.anyio
async def test_openapi_schema_contains_security_scheme():
    """Verify the OpenAPI schema includes BearerAuth security scheme."""
    schema = app.openapi()
    assert "components" in schema
    assert "securitySchemes" in schema["components"]
    schemes = schema["components"]["securitySchemes"]
    assert "BearerAuth" in schemes
    bearer_auth = schemes["BearerAuth"]
    assert bearer_auth["type"] == "http"
    assert bearer_auth["scheme"] == "bearer"
    assert bearer_auth["bearerFormat"] == "JWT"


@pytest.mark.anyio
async def test_openapi_schema_security_requirement_on_protected_endpoint():
    """Verify a protected endpoint has security requirement."""
    schema = app.openapi()
    # Find path /api/v1/users/me
    path = "/api/v1/users/me"
    assert path in schema["paths"]
    get_op = schema["paths"][path].get("get", {})
    # Should have security requirement referencing BearerAuth
    assert "security" in get_op
    security = get_op["security"]
    # Expect [{"BearerAuth": []}]
    assert any("BearerAuth" in s for s in security)


@pytest.mark.anyio
async def test_openapi_schema_no_security_on_auth_endpoint():
    """Verify auth endpoints do NOT have security requirement."""
    schema = app.openapi()
    # Login endpoint
    path = "/api/v1/auth/login"
    assert path in schema["paths"]
    post_op = schema["paths"][path].get("post", {})
    # Should NOT have security requirement
    assert "security" not in post_op or post_op.get("security") == []
    # Register endpoint
    path = "/api/v1/auth/register"
    assert path in schema["paths"]
    post_op = schema["paths"][path].get("post", {})
    assert "security" not in post_op or post_op.get("security") == []


@pytest.mark.anyio
async def test_swagger_ui_accessible(test_client: AsyncClient):
    """Verify Swagger UI page loads."""
    response = await test_client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
