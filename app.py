import os

from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


load_dotenv()

app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)


templates = Jinja2Templates(directory="templates")


ALGOLIA_APP_ID = os.environ["ALGOLIA_APP_ID"]
ALGOLIA_API_KEY = os.environ["ALGOLIA_API_KEY"]

algolia_client = SearchClient.create(
    ALGOLIA_APP_ID,
    ALGOLIA_API_KEY,
)


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
    index = algolia_client.init_index("zara_products")
    results = index.search(
        search_query,
        {
            "page": 1,
            "hitsPerPage": 12,
        },
    )
    return results["hits"]
