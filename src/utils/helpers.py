"""Helper functions for the project"""

import uuid
from datetime import datetime


class Helpers:
    """Helpers class."""

    @staticmethod
    async def generate_uuid() -> str:
        """Generate uuid for user id."""
        return str(uuid.uuid4())

    @staticmethod
    def normalize_datetime(dt: datetime) -> datetime:
        """Ensure the datetime is timezone-aware and converted to UTC."""
        if dt.tzinfo is None:
            # Assume naive datetime is in UTC
            return dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
