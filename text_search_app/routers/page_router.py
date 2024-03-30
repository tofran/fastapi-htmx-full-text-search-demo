from typing import Literal

from fastapi import APIRouter, Query, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from text_search_app.search_indexes.algolia import get_items
from text_search_app.templates import make_template_response

router = APIRouter(
    prefix="",
)


@router.get(
    "/healthz",
    response_model=Literal["OK"],
    tags=["Others"],
)
async def health_check():
    return Response(
        "OK",
        media_type="text/plain",
    )


@router.get(
    "/robots.txt",
    tags=["Others"],
)
async def get_robots_txt():
    return Response(
        "User-agent: *\nDisallow: /html-api",
        media_type="text/plain",
    )


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["Front-end HTML pages"],
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
