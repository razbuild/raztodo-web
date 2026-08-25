from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from raztodo.infrastructure.version import get_version

from raztodo_web.features.explain.routes import router as explain_router
from raztodo_web.features.tasks.routes import router as tasks_router

_WEB_DIR = Path(__file__).resolve().parent.parent / "web"
_STATIC_DIR = _WEB_DIR / "static"
_TEMPLATES_DIR = _WEB_DIR / "templates"


app = FastAPI(
    title="RazTodo",
    description="Local web interface for RazTodo",
    version=get_version(),
)

app.mount(
    "/static",
    StaticFiles(directory=_STATIC_DIR),
    name="static",
)

templates = Jinja2Templates(directory=_TEMPLATES_DIR)

app.include_router(tasks_router)
app.include_router(explain_router)


@app.get("/", include_in_schema=False)
async def index(request: Request):
    """Serve the single-page UI, rendered from templates/index.html."""
    return templates.TemplateResponse(request, "index.html")
