from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from text_search_app.config import DEVELOPMENT_MODE, ENABLE_INDEX_MANAGEMENT
from text_search_app.routers import (
    html_api_router,
    index_management_router,
    misc_router,
    page_router,
)
from text_search_app.search_indexes import sqlite_index
from text_search_app.templates import make_template_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    sqlite_index.setup_db()
    yield


app = FastAPI(
    title="Python FastAPI HTMX full-text-search demo",
    debug=DEVELOPMENT_MODE,
    openapi_url="/openapi.json" if DEVELOPMENT_MODE else None,
    lifespan=lifespan,
)


app.include_router(page_router.router)
app.include_router(html_api_router.router)

if ENABLE_INDEX_MANAGEMENT:
    app.include_router(index_management_router.router)

app.include_router(misc_router.router)


app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)


@app.exception_handler(StarletteHTTPException)
async def not_found_exception_handler(
    request: Request,
    exception: BaseException,
):
    return make_template_response(
        "404",
        request,
    )
