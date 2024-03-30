from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from text_search_app.config import DEVELOPMENT_MODE
from text_search_app.routers import html_api_router, index_management_router, page_router
from text_search_app.templates import make_template_response

app = FastAPI(
    title="Search sample",
    debug=DEVELOPMENT_MODE,
    openapi_url="/openapi.json" if DEVELOPMENT_MODE else None,
)


app.include_router(page_router.router)
app.include_router(index_management_router.router)
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
