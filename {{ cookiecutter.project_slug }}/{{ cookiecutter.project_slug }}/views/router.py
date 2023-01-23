from fastapi import APIRouter

from {{ cookiecutter.project_slug }}.views.endpoints import {{ cookiecutter.first_model }}s

views_router = APIRouter()
views_router.include_router({{ cookiecutter.first_model }}s.router, tags=["Views"])
