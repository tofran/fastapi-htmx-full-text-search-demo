from fastapi import APIRouter, Depends, Header, Query, Request, status
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from text_search_app.config import PREVENT_HTML_API_DIRECT_ACCESS
from text_search_app.search_indexes.indexes import SearchIndex, get_items
from text_search_app.templates import make_template_response


async def prevent_html_api_direct_access(
    hx_request_header: bool = Header(
        alias="HX-Request",
        default_factory=lambda: False,
        openapi_examples={
            "true required (cannot be changed)": {
                "value": True,
            }
        },
    ),
) -> None:
    """
    Asserts that the HTML API is not accessed directly via the browser.
    This is disabled when `DEVELOPMENT_MODE` is True.
    """

    if PREVENT_HTML_API_DIRECT_ACCESS and not hx_request_header:
        # Simulate a 404 just for demonstration (I'm avoiding custom errors in this project)
        raise StarletteHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )


router = APIRouter(
    prefix="/html-api",
    tags=["HTML API"],
    dependencies=[Depends(prevent_html_api_direct_access)],
)


@router.get(
    "/items",
    response_class=HTMLResponse,
)
async def get_items_html(
    request: Request,
    search_index: SearchIndex = Query(
        default=SearchIndex.SQLITE,
        description="The search index to use",
    ),
    search_query: str = Query(
        default="",
        description="The user query to find products that better match it",
    ),
):
    return make_template_response(
        "results",
        request,
        {
            "items": get_items(
                search_index=search_index,
                search_query=search_query,
            )
        },
    )
