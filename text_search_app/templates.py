from typing import Any

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def make_template_response(
    template_name: str,
    request: Request,
    template_data: dict[str, Any] | None = None,
) -> HTMLResponse:
    template_data = {} if template_data is None else template_data

    return templates.TemplateResponse(
        name=f"{template_name}.jinja.html",
        context={
            **template_data,
            "request": request,
        },
    )
