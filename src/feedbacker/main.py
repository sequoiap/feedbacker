import time
import logging
from os import path
from uuid import uuid1
from typing import Optional, Final
# from contextvars import ContextVar

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from jinja2 import Environment, FileSystemLoader

# from sqlalchemy import inspect
# from sqlalchemy.orm import scoped_session
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.routing import compile_path
from starlette.responses import Response, StreamingResponse, FileResponse

from .api import api_router
from .config import (
    ROOT_DIR,
    STATIC_DIR,
    TEMPLATE_DIR,
)
from .frontend import frontend
# from .database.core import engine, sessionmaker
# from .extensions import configure_extensions
# from .logging import configure_logging
# from .metrics import provider as metric_provider
# from .rate_limiter import limiter


log = logging.getLogger(__name__)

# we configure the logging level and format
# configure_logging()

# we configure the extensions such as Sentry
# configure_extensions()


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )


exception_handlers = {404: not_found}

# we create the ASGI for the app
app = FastAPI(exception_handlers=exception_handlers, openapi_url="")
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# we create the Web API framework
api = FastAPI(
    title="Feedbacker",
    description="Welcome to feedbacker's API documentation! Here you will able to discover all of the ways you can interact with the feedbacker API.",
    root_path="/api/v1",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)
api.add_middleware(GZipMiddleware, minimum_size=1000)


# we add all API routes to the Web API framework
api.include_router(api_router)

# we mount the frontend and app
# if STATIC_DIR and path.isdir(STATIC_DIR):
#     frontend.mount("/", StaticFiles(directory=STATIC_DIR), name="app")

app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
