"""User routes."""

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.database import get_repository
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.db.repositories.user import UserRepository
from src.models.token import AccessToken
from src.models.user import UserCreate, UserInDb, UserPublic

user_router = APIRouter()


@user_router.post(
    "",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    new_user: UserCreate,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDb:
    """Register a new user."""
    return await user_repo.create_user(new_user=new_user)


@user_router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def user_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> AccessToken:
    """Login user."""
    form_data.username = form_data.username.lower()
    token = await user_repo.login(form_data)
    response.set_cookie(
        "access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return token


@user_router.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    user: UserInDb = Depends(get_current_user),
) -> UserInDb:
    """Get the current user."""
    return user
