from typing import Literal

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="",
    tags=["Miscellaneous"],
)


@router.get(
    "/healthz",
    response_model=Literal["OK"],
)
async def health_check():
    return Response(
        "OK",
        media_type="text/plain",
    )


@router.get(
    "/robots.txt",
    response_class=PlainTextResponse,
)
async def get_robots_txt():
    return PlainTextResponse(
        "User-agent: *\nDisallow: /html-api",
        media_type="text/plain",
    )
