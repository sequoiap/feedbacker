from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from jinja2 import Environment, FileSystemLoader

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.routing import compile_path
from starlette.responses import Response, StreamingResponse, FileResponse

from feedbacker.assignments.views import frontend as assignments_frontend
from .config import (
    STATIC_DIR,
    templates,
)


# we create the ASGI for the frontend
frontend = FastAPI(openapi_url="")
frontend.add_middleware(GZipMiddleware, minimum_size=1000)
frontend.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    # if response.status_code == 404:
    #     if STATIC_DIR:
    #         return FileResponse(path.join(STATIC_DIR, "index.html"))
    return response



@frontend.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={}
    )

# @frontend.get("/assignments", response_class=HTMLResponse)
# async def assignments(request: Request):
#     return templates.TemplateResponse(
#         request=request, name="assignment.html", context={}
#     )

frontend.mount("/assignments", app=assignments_frontend, name="assignments")
