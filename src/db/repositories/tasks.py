"""Database Connect Tasks"""

from databases import Database
from fastapi import FastAPI

from src.core.config import DATABASE_URL


async def connect_database(app: FastAPI) -> None:
    """Connect to DB"""
    try:
        database = Database(DATABASE_URL)
        await database.connect()
        app.state._db = database
        print("Connected to postgres database. ")
    except Exception as e:
        print("Failed to connect to postgres database", e)


async def disconnect_database(app: FastAPI) -> None:
    """Close db."""
    try:
        await app.state._db.disconnect()
        print("Disconnected from postgres database. ")
    except Exception as e:
        print("Error disconnecting from postgres", e)
