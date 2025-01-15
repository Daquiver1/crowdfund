"""Decorator for get db operations to handle database exceptions."""

import logging
from functools import wraps
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from typing import Any

from src.errors.core import InternalServerError, InvalidTokenError
from src.errors.database import (
    AlreadyExistsError,
    BadRequestError,
    ForeignKeyError,
    GeneralDatabaseError,
    IncorrectCredentialsError,
    NotFoundError,
)

audit_entities = ["profile", "user"]
audit_logger = logging.getLogger("audit")
app_logger = logging.getLogger("app")


def handle_get_database_exceptions(entity_name: str) -> callable:  # type: ignore
    """Decorator to handle database exceptions for get operations in SQLite."""

    def decorator(func: callable) -> callable:  # type: ignore
        @wraps(func)
        async def wrapper(
            self, *args: tuple, **kwargs: dict[str, Any]  # noqa
        ) -> callable:  # type: ignore
            logger = (
                audit_logger if entity_name.lower() in audit_entities else app_logger
            )
            try:
                return await func(self, *args, **kwargs)
            except OperationalError as e:
                logger.exception(f"OperationalError for {entity_name}", exc_info=True)
                raise GeneralDatabaseError(entity_name=entity_name) from e
            except ProgrammingError as e:
                logger.exception(f"ProgrammingError for {entity_name}", exc_info=True)
                raise BadRequestError(
                    f"Bad Request: Invalid details for {entity_name}"
                ) from e
            except ValueError as e:
                logger.exception(f"ValueError for {entity_name}", exc_info=True)
                raise BadRequestError(
                    f"Bad Request: Invalid details for {entity_name}"
                ) from e
            except NotFoundError:
                logger.exception(f"NotFoundError for {entity_name}")
                raise
            except IncorrectCredentialsError:
                logger.exception(f"Incorrect credentials for {entity_name}")
                raise
            except InvalidTokenError:
                logger.exception(f"Invalid jwt token for {entity_name}")
                raise
            except Exception as e:
                logger.exception(f"Unexpected error for {entity_name}", exc_info=True)
                raise InternalServerError(
                    additional_message="Unexpected error. Try again."
                ) from e

        return wrapper

    return decorator


def handle_post_database_exceptions(
    entity_name: str, foreign_key_entity: str = "", already_exists_entity: str = ""
) -> callable:  # type: ignore
    """Decorator to handle database exceptions for post operations in SQLite."""

    def decorator(func: callable) -> callable:  # type: ignore

        @wraps(func)
        async def wrapper(
            self, *args: tuple, **kwargs: dict[str, Any]  # noqa
        ) -> callable:  # type: ignore
            logger = (
                audit_logger if entity_name.lower() in audit_entities else app_logger
            )
            try:
                return await func(self, *args, **kwargs)
            except IntegrityError as e:
                logger.exception(f"IntegrityError for {entity_name}", exc_info=True)
                if "UNIQUE constraint failed" in str(e):
                    raise AlreadyExistsError(entity_name=already_exists_entity) from e
                elif "FOREIGN KEY constraint failed" in str(e):
                    raise ForeignKeyError(entity_name=foreign_key_entity) from e
                else:
                    raise GeneralDatabaseError(entity_name=entity_name) from e
            except OperationalError as e:
                logger.exception(f"OperationalError for {entity_name}", exc_info=True)
                raise GeneralDatabaseError(entity_name=entity_name) from e
            except ValueError as e:
                logger.exception(f"ValueError for {entity_name}", exc_info=True)
                raise BadRequestError(
                    f"Bad Request: Invalid details for {entity_name}"
                ) from e
            except NotFoundError:
                logger.exception(f"NotFoundError for {entity_name}")
                raise
            except IncorrectCredentialsError:
                logger.exception(f"Incorrect credentials for {entity_name}")
                raise
            except InvalidTokenError:
                logger.exception(f"Invalid jwt token for {entity_name}")
                raise
            except Exception as e:
                logger.exception(f"Unexpected error for {entity_name}", exc_info=True)
                raise InternalServerError(
                    additional_message="Unexpected error. Try again."
                ) from e

        return wrapper

    return decorator
