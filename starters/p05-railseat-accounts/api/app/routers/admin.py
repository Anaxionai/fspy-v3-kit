"""Admin routes: users and roles (P5 add-on, task 11).

Include it in app/main.py with `app.include_router(admin.router)` (task 11).
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth_schemas import RoleIn, UserOut
from app.db import get_session
from app.models import User
from app.security import current_user

# TODO(task 11): close the whole router to everyone but admins. Give APIRouter the
# `dependencies=[...]` setting from the brief's step 5, using require_role().
router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(session: AsyncSession = Depends(get_session)):
    """Every user with `id`, `email` and `role`, in id order (task 11, step 5)."""
    raise NotImplementedError("TODO(task 11): list the users")


@router.patch("/users/{user_id}/role", response_model=UserOut)
async def change_role(
    user_id: int,
    data: RoleIn,
    request: Request,
    admin: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
):
    """Give user `user_id` the role `data.role` and return the user (task 11, step 5).

    An unknown user gets 404. `admin` is the admin who makes the change.
    """
    # TODO(task 14): log role_changed with log_event(), naming the user whose role changed.
    raise NotImplementedError("TODO(task 11): change the user's role")
