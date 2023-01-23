from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from {{ cookiecutter.project_slug }} import crud
from {{ cookiecutter.project_slug }}.api.deps import get_db

router = APIRouter()
templates = Jinja2Templates(directory="{{ cookiecutter.project_slug }}/views/templates")


@router.get("/{{ cookiecutter.first_model }}s", summary="Returns HTML Response with the {{ cookiecutter.first_model }}", response_class=HTMLResponse)
async def html_view_{{ cookiecutter.first_model }}s(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Returns HTML response with list of {{ cookiecutter.first_model }}s.

    Args:
        request(Request): The request object
        db(Session): The database session.

    Returns:
        Response: HTML page with the {{ cookiecutter.first_model }}s

    """
    {{ cookiecutter.first_model }}s = await crud.{{ cookiecutter.first_model }}.get_all(db=db)
    {{ cookiecutter.first_model }}s_context = [
        {
            "id": {{ cookiecutter.first_model }}.id,
            "title": {{ cookiecutter.first_model }}.title,
            "url": {{ cookiecutter.first_model }}.url,
        }
        for {{ cookiecutter.first_model }} in {{ cookiecutter.first_model }}s
    ]
    context = {"request": request, "{{ cookiecutter.first_model }}s": {{ cookiecutter.first_model }}s_context}
    return templates.TemplateResponse("view_{{ cookiecutter.first_model }}s.html", context)
