"""Base message handler for the WhatsApp bot."""

from abc import ABC, abstractmethod
from typing import Optional

from databases import Database

from src.services.redis_client import RedisClient


class BaseMessageHandler(ABC):
    """Base message handler for the WhatsApp bot."""

    def __init__(self, redis_client: RedisClient, db: Database) -> None:
        """Initialize the handler with necessary dependencies."""
        self.redis_client = redis_client
        self.db = db

    @abstractmethod
    async def handle_message(
        self, user_id: str, whatsapp_id: str, message: str
    ) -> Optional[str]:
        """Handle a message from a user."""
        pass
