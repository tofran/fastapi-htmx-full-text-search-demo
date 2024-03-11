from typing import Literal

from fastapi import FastAPI, Query, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from text_search_app.algolia_search import get_items


app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)


templates = Jinja2Templates(directory="templates")


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
    return templates.TemplateResponse(
        "index.jinja.html",
        {
            "request": request,
            "items": get_items(search_query),
        },
    )


@app.get(
    "/html-api/items",
    response_class=HTMLResponse,
    tags=["HTML API"],
)
async def get_items_html(
    request: Request,
    search_query: str = Query(
        default="",
    ),
):
    return templates.TemplateResponse(
        "results.jinja.html",
        {
            "request": request,
            "items": get_items(search_query),
        },
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
