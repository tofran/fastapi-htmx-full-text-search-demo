from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from text_search_app.search_indexes import indexes
from text_search_app.templates import make_template_response

router = APIRouter(
    prefix="",
    tags=["Front-end HTML pages"],
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def get_index_html(
    request: Request,
    # TODO: later one could add a search_query query params to preserve the user state
):
    return make_template_response(
        "index",
        request,
        {
            "items": indexes.get_items(
                search_query=None,
            ),
        },
    )
