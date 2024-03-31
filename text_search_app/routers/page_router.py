from fastapi import APIRouter, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from text_search_app.search_indexes.indexes import SearchIndex, get_items
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
    selected_search_index: SearchIndex = Query(
        alias="search_index",
        default=SearchIndex.SQLITE,
        description="The search index to use",
    ),
    search_query: str = Query(
        default="",
        description="The user query to find products that better match it",
    ),
):
    return make_template_response(
        "index",
        request,
        {
            "search_query": search_query,
            "search_indexes": [
                {
                    "name": search_index.name,
                    "is_selected": selected_search_index == search_index,
                }
                for search_index in SearchIndex
            ],
            "items": get_items(
                search_index=selected_search_index,
                search_query=search_query,
            ),
        },
    )
