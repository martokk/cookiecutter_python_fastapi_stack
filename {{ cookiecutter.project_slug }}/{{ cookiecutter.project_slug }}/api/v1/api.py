from fastapi import APIRouter

from {{ cookiecutter.project_slug }}.api.v1.endpoints import login, users, {{ cookiecutter.first_model }}

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router({{ cookiecutter.first_model }}.router, prefix="/{{ cookiecutter.first_model }}", tags=["{{ cookiecutter.first_model }}s"])
