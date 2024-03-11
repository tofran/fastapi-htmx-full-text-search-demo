from fastapi import FastAPI, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

ITEMS = [
    {"title": "Hello world", "description": "sample"},
    {"title": "hello 2", "description": "sample"},
    {"title": "hello 2", "description": "sample"},
    {"title": "hello 2", "description": "sample"},
    {"title": "hello 2", "description": "sample"},
    {"title": "hello 2", "description": "sample"},
    {"title": "Sample item", "description": "sample"},
]


@app.get(
    "/",
    response_class=HTMLResponse,
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


def get_items(search_query: str):
    return [
        item  # fmt: skip
        for item in ITEMS
        if search_query == "" or search_query in item["title"]
    ]
