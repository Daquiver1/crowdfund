"""Formatters module."""


class Formatters:
    """Formatters class"""

    @staticmethod
    def format_database_url(db_url: str) -> str:
        """Removes '+asyncpg' from the database URL if present."""
        if "+asyncpg" in db_url:
            modified_url = db_url.replace("+asyncpg", "")
            return modified_url
        else:
            return db_url
