"""User repository."""

from typing import Optional
from uuid import UUID

from databases import Database
from fastapi.security import OAuth2PasswordRequestForm

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.errors.database import (
    FailedToCreateEntityError,
    IncorrectCredentialsError,
    NotFoundError,
)
from src.models.token import AccessToken
from src.models.user import UserCreate, UserInDb
from src.services.auth import AuthService

CREATE_USER_QUERY = """
    INSERT INTO users (email, first_name, last_name, username, password_hash)
    VALUES (:email, :first_name, :last_name, :username, :password_hash)
    RETURNING user_id, email, first_name, last_name, username, password_hash, created_at, updated_at, is_deleted;
"""

GET_USER_BY_ID_QUERY = """
    SELECT user_id, email, first_name, last_name, username, password_hash, created_at, updated_at, is_deleted
    FROM users
    WHERE user_id = :user_id AND is_deleted = FALSE;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT user_id, email, first_name, last_name, username, password_hash, created_at, updated_at, is_deleted
    FROM users
    WHERE email = :email AND is_deleted = FALSE;
"""

GET_USER_BY_USERNAME_QUERY = """
    SELECT user_id, email, first_name, last_name, username, password_hash, created_at, updated_at, is_deleted
    FROM users
    WHERE username = :username AND is_deleted = FALSE;
"""


class UserRepository(BaseRepository):
    """Contains logic for all user operations."""

    def __init__(self, db: Database) -> None:
        """Initializes the UserRepository with the database instance."""
        super().__init__(db)

    @handle_post_database_exceptions("User", already_exists_entity="User email")
    async def create_user(self, *, new_user: UserCreate) -> UserInDb:
        """Creates a new user."""
        created_user = await self.db.fetch_one(
            query=CREATE_USER_QUERY, values=new_user.model_dump()
        )
        if not created_user:
            raise FailedToCreateEntityError(entity_name="User.")
        return UserInDb(**created_user)  # type: ignore

    async def login(self, user_request: OAuth2PasswordRequestForm) -> AccessToken:
        """Logs in a user."""
        user = await self.get_user(username=user_request.username)

        if not user or not await AuthService().verify_password(
            user_request.password, user.password_hash
        ):
            raise IncorrectCredentialsError()

        access_token = AuthService().create_access_token(
            data={"user_id": str(user.user_id)}
        )

        return AccessToken(
            access_token=access_token,
            token_type="bearer",
        )

    @handle_get_database_exceptions("User")
    async def get_user(
        self,
        user_id: Optional[UUID] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ) -> UserInDb:
        """Retrieves a user by their ID."""
        search_criteria = {
            "user_id": (GET_USER_BY_ID_QUERY, user_id),
            "email": (GET_USER_BY_EMAIL_QUERY, email),
            "username": (GET_USER_BY_USERNAME_QUERY, username),
        }

        for field, (query, value) in search_criteria.values():
            if value:
                user_record = await self.db.fetch_one(
                    query=query, values={field: value}
                )
                if user_record:
                    return UserInDb(**user_record)  # type: ignore
                else:
                    raise NotFoundError(entity_name="user", entity_identifier=value)

        raise ValueError("No search criteria provided")
