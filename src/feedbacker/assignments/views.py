from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from dispatch.database.core import DbSession
# from dispatch.database.service import CommonParameters, search_filter_sort_paginate
# from dispatch.auth.permissions import SensitiveProjectActionPermission, PermissionsDependency
# from dispatch.models import PrimaryKey

# from .models import (
#     CaseCostTypeCreate,
#     CaseCostTypePagination,
#     CaseCostTypeRead,
#     CaseCostTypeUpdate,
# )
from feedbacker.config import templates

from .schemas import AssignmentCreate, AssignmentRead, AssignmentUpdate
from .service import create, delete, get, update

api_router = APIRouter()
frontend = FastAPI(debug=True)


@frontend.get("/", response_class=HTMLResponse)
async def assignments(request: Request):
    return templates.TemplateResponse(
        request=request, name="assignment.html", context={}
    )

# @router.get("/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="assignment.html", context={"id": id}
#     )
