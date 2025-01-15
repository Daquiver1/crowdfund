"""Setting up configs."""

# Third party imports
import logging
import sys

from starlette.config import Config

config = Config(".env")


# Project configs
PROJECT_NAME = "crowdfund"
VERSION = "1.0"
API_PREFIX = "/api/v1"

# Environment
ENV = config("ENV", cast=str, default="DEV")

# Database[Postgres]
POSTGRES_USERNAME = config("POSTGRES_USERNAME", cast=str, default="")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default="")
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="")

if ENV == "PROD":
    DATABASE_URL = config("PROD_DATABASE_URL", cast=str, default="")
else:
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60
)
SECRET_KEY = config("SECRET_KEY", cast=str, default="")
ALGORITHM = config("ALGORITHM", cast=str, default="HS256")


def configure_logging() -> None:
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
