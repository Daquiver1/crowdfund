"""Middleware configuration for the application."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

request_logger = logging.getLogger("request")


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware."""
    # origins = ["http://localhost:3000"]
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: callable) -> JSONResponse:  # type: ignore
        client_ip = request.client.host  # type: ignore
        method = request.method
        path = request.url.path
        request_logger.info(f"Incoming request: {method} {path} from {client_ip}")

        response = await call_next(request)

        status_code = response.status_code
        request_logger.info(f"Response: {status_code}")

        return response