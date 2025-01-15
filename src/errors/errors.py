"""Custom error classes for handling database errors."""

from starlette import status


class DatabaseError(Exception):
    """Base class for database errors."""

    def __init__(self, message: str, status_code: int) -> None:
        """Initializes the error with a message and status code."""
        self.message = message
        self.status_code = status_code


class AlreadyExistsError(DatabaseError):
    """Raised when trying to create a duplicate entity."""

    def __init__(self, entity_name: str) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = f"{entity_name.capitalize()} with this data already exists"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class NotFoundError(DatabaseError):
    """Raised when an entity is not found in the database."""

    def __init__(self, entity_name: str) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = f"{entity_name.capitalize()} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class IncorrectCredentialsError(DatabaseError):
    """Raised when an entity is not found in the database."""

    def __init__(self) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = "Incorrect credentials"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class InvalidTokenError(DatabaseError):
    """Raised when an entity is not found in the database."""

    def __init__(self) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = "Invalid token"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ForeignKeyError(DatabaseError):
    """Raised when trying to delete an entity with foreign key constraints."""

    def __init__(self, entity_name: str) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = f"{entity_name.capitalize()} has foreign key constraints"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class FailedToCreateEntityError(DatabaseError):
    """Raised when trying to delete an entity with foreign key constraints."""

    def __init__(self, entity_name: str) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = f"Failed to create {entity_name.capitalize()}"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class FailedToCreateUpdateQueryError(DatabaseError):
    """Raised when trying to delete an entity with foreign key constraints."""

    def __init__(self, entity_name: str) -> None:
        """Initializes the error with the entity name and a dynamic message."""
        message = f"Failed to create update query for {entity_name.capitalize()}"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class InternalServerError(DatabaseError):
    """Raised for internal database errors."""

    def __init__(self, message: str = "Database error") -> None:
        """Initializes the error with a message."""
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)
