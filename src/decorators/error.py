"""Registration errors decorator for the WhatsApp bot."""

from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def handle_registration_errors(
    location: str,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to handle errors for registration methods."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:

        @wraps(func)
        async def wrapper(self: object, *args: str, **kwargs: dict[str, Any]) -> T:
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error in {location}: {e}")

        return wrapper

    return decorator


def handle_errors(
    location: str, clear_states: bool = False
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to handle errors for search methods."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:

        @wraps(func)
        async def wrapper(self: object, *args: str, **kwargs: dict[str, Any]) -> T:
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error in {location}: {e}")

        return wrapper

    return decorator
