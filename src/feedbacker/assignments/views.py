from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
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
from feedbacker.auth.service import CurrentUser, decode_token
from feedbacker.config import templates
from feedbacker.database import DbSession, SessionLocal
from feedbacker.config import AUTH_COOKIE_NAME

from .schemas import AssignmentCreate, AssignmentRead, AssignmentUpdate
from .service import get_all_assignments, get_assignment


api_router = APIRouter()


@api_router.get("/")
async def get_assignments(
    db_session: DbSession,
    current_user: CurrentUser,
    course_id: int = None,
) -> list[AssignmentRead]:
    """Get all assignments."""
    return get_all_assignments(db_session, course_id)


@api_router.get("/{assn_id}")
async def get_one_assignment(
    assn_id: int,
    db_session: DbSession,
    current_user: CurrentUser,
) -> AssignmentRead:
    """Get a specific assignment."""
    return get_assignment(db_session, assn_id)


@api_router.post("/attempts/{attempt_id}")
async def end_attempt(
    attempt_id: int,
    db_session: DbSession,
    current_user: CurrentUser,
) -> list[AssignmentRead]:
    """Terminate an attempt."""
    # return get_all_assignments(db_session)
    return []


@api_router.websocket("/grader_ws")
async def grader_ws(
    websocket: WebSocket,
):
    """Websocket for grading."""
    await websocket.accept()
    with SessionLocal() as session:
        try:
            user = decode_token(session, websocket.cookies.get(AUTH_COOKIE_NAME))
            await websocket.send_text(f"Hello, {user.firstname}. We're grading your assignment...")
        except HTTPException as e:
            await websocket.send_text(f"Error: {e}")
            await websocket.close()
            return

    while True:
        try:
            data = await websocket.receive_text()
            with SessionLocal() as session:
                print("We've got a db here")
                print(session)
            await websocket.send_text(f"Message text was: {data}")
            if data == "quit":
                await websocket.close()
                break
        except WebSocketDisconnect:
            print("Websocket closed")
            break
