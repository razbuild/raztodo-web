from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi.routing import Mount
from httpx import ASGITransport, AsyncClient

from raztodo_web.app import dependencies as deps
from raztodo_web.app.factory import app

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncClient:
    """AsyncClient with just enough use cases mocked to avoid hitting real infra."""
    list_uc = MagicMock()
    list_uc.execute.return_value = []
    explain_uc = MagicMock()
    explain_uc.stream.return_value = []

    app.dependency_overrides[deps.get_list_uc] = lambda: list_uc
    app.dependency_overrides[deps.get_explain_uc] = lambda: explain_uc

    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c
    finally:
        app.dependency_overrides.clear()


class TestAppMetadata:
    def test_title(self) -> None:
        assert app.title == "RazTodo"

    def test_description(self) -> None:
        assert app.description == "Local web interface for RazTodo"

    def test_version_is_set(self) -> None:
        assert app.version


class TestStaticMount:
    def test_static_is_mounted(self) -> None:
        mounts = [route for route in app.routes if isinstance(route, Mount)]
        assert any(
            route.path == "/static" and route.name == "static" for route in mounts
        )


class TestRouters:
    """Smoke-check that both feature routers are wired into the app.

    We hit a real endpoint instead of introspecting app.routes, because
    FastAPI >=0.137 stores included routers as internal `_IncludedRouter`
    wrappers that don't expose `.path`. An actual request is stable
    regardless of FastAPI's internal routing representation.
    """

    async def test_tasks_router_included(self, client: AsyncClient) -> None:
        response = await client.get("/api/tasks")
        assert response.status_code != 404

    async def test_explain_router_included(self, client: AsyncClient) -> None:
        response = await client.get("/api/tasks/1/explain")
        assert response.status_code != 404


class TestIndexRoute:
    async def test_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/")
        assert response.status_code == 200

    async def test_returns_html(self, client: AsyncClient) -> None:
        response = await client.get("/")
        assert response.headers["content-type"].startswith("text/html")

    def test_excluded_from_openapi_schema(self) -> None:
        schema = app.openapi()
        assert "/" not in schema["paths"]
