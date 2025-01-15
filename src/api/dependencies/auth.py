"""Dependency for authentication."""

import logging

from databases import Database
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.database import get_database
from src.db.repositories.user import UserRepository
from src.models.user import UserInDb
from src.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)
app_logger = logging.getLogger("app")


async def get_auth_service() -> AuthService:
    """Auth Service Dependency."""
    return AuthService()


async def get_user_repository(db: Database = Depends(get_database)) -> UserRepository:
    """User Repository Dependency."""
    return UserRepository(db)


async def get_token_from_cookies(request: Request) -> str:
    """Get the access and refresh tokens from the cookies."""
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials. Token not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token


async def get_current_user(
    access_token: str = Depends(get_token_from_cookies),
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserInDb:
    """Get the current user from the access token."""
    try:
        user_id = await auth_service.verify_token(access_token)
    except Exception as e:
        app_logger.exception("Access token verification failed", exc_info=e)
        raise HTTPException(  # noqa
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    user = await user_repo.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user
