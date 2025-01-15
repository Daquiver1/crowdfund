"""Route configuration for the application."""

from fastapi import FastAPI

from src.core.config import API_PREFIX


def setup_routes(app: FastAPI) -> None:
    """Configure all application routes."""
    from src.api.routes.project import project_router
    from src.api.routes.user import user_router

    api_prefix = API_PREFIX

    app.include_router(user_router, prefix=f"{api_prefix}/users", tags=["User"])
    app.include_router(
        project_router, prefix=f"{api_prefix}/projects", tags=["Project"]
    )

    @app.get("/", name="index")
    async def index() -> str:
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."
