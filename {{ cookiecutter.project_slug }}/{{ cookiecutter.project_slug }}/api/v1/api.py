from fastapi import APIRouter

from {{ cookiecutter.project_slug }} import models, settings, version
from {{ cookiecutter.project_slug }}.api.v1.endpoints import login, users, {{ cookiecutter.first_model }}

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router({{ cookiecutter.first_model }}.router, prefix="/{{ cookiecutter.first_model }}", tags=["{{ cookiecutter.first_model | title }}s"])


@api_router.get("/", response_model=models.HealthCheck, tags=["status"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict[str, str]: Health check response.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": version,
        "description": settings.PROJECT_DESCRIPTION,
    }
