"""Route configuration for the application."""

from fastapi import FastAPI

from src.core.config import ENV


def setup_routes(app: FastAPI) -> None:
    """Configure all application routes."""

    @app.get("/", name="index")
    async def index() -> str:
        print("This is the env", ENV)
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."
