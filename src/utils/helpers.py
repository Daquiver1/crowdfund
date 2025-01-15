"""Helper functions for the project"""

import uuid


class Helpers:
    """Helpers class."""

    @staticmethod
    async def generate_uuid() -> str:
        """Generate uuid for user id."""
        return str(uuid.uuid4())
