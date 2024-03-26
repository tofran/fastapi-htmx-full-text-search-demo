from typing import Literal

from fastapi import FastAPI, Query, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from text_search_app import html_api_router
from text_search_app.algolia_search import get_items
from text_search_app.config import DEVELOPMENT_MODE
from text_search_app.templates import make_template_response

app = FastAPI(
    title="Search sample",
    debug=DEVELOPMENT_MODE,
    openapi_url="/openapi.json" if DEVELOPMENT_MODE else None,
)


app.include_router(html_api_router.router)


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


@app.get(
    "/healthz",
    response_model=Literal["OK"],
    tags=["Others"],
)
async def health_check():
    return Response(
        "OK",
        media_type="text/plain",
    )


@app.get(
    "/robots.txt",
    tags=["Others"],
)
async def get_robots_txt():
    return Response(
        "User-agent: *\nDisallow: /html-api",
        media_type="text/plain",
    )


@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["Search"],
)
async def get_index_html(
    request: Request,
    search_query: str = Query(
        default="",
    ),
):
    return make_template_response(
        "index",
        request,
        {
            "items": get_items(search_query),
        },
    )
