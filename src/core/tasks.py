"""Core task: Connect and Disconnect to db when application starts and stops."""

# Standard library imports
from typing import Callable

# Third party imports is right
from fastapi import FastAPI

from src.core.config import configure_logging
from src.db.repositories.tasks import connect_database, disconnect_database


def create_start_app_handler(app: FastAPI) -> Callable:
    """Connect to db."""

    async def start_app() -> None:
        print("Starting app.")
        await connect_database(app)
        configure_logging()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Disconnect db."""

    async def stop_app() -> None:
        await disconnect_database(app)

    return stop_app
