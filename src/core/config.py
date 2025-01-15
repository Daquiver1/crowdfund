"""Setting up configs."""

# Third party imports
import logging
import sys

from databases import DatabaseURL
from starlette.config import Config

config = Config(".env")


# Project configs
PROJECT_NAME = "crowdfund"
VERSION = "1.0"
API_PREFIX = "/api/v1"

# Environment
ENV = config("ENV", cast=str, default="DEV")

# Database[Postgres]
if ENV == "DEV":
    DATABASE_URL = config(
        "DATABASE_URL",
        cast=DatabaseURL,
        default="",
    )
elif ENV == "PROD":
    DATABASE_URL = config(
        "PROD_DATABASE_URL",
        cast=DatabaseURL,
        default="",
    )


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
