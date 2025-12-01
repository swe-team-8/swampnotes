from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from collections.abc import Generator

from fastapi import Depends, HTTPException, status, Query
from sqlmodel import Session

from .db import get_session, get_or_create_user
from .models import User

# This file gives us a single place to import dependencies when creating/developing routers
# i.e. can cleanly give a router access to auth + jwt/database as necessary w/o messy imports

# Re-export names from .auth
from .auth import (  # noqa: F401
    require_user,
    optional_user,
    require_admin,
    TokenUser,
)

# Re-export commonly used models
from .models import (  # noqa: F401
    Note,
    Course,
    Purchase,
)

# Re-export commonly used DB functions
from .db import (  # noqa: F401
    create_note,
    search_notes,
    get_user_purchased_notes,
    get_user_uploaded_notes,
    create_purchase,
    has_purchased_note,
    create_course,
    get_all_courses,
    get_all_notes,
)

# Re-export MinIO functions
from .minio_client import (  # noqa: F401
    upload_bytes_to_minio,
    get_file_from_minio,
    delete_from_minio,
    presign_put,
    presign_get,
)


def db_session() -> Generator[Session, None, None]:
    yield from get_session()


def get_current_db_user(
    token: TokenUser = Depends(require_user), session: Session = Depends(db_session)
) -> User:
    # Get or create DB user from authenticated Clerk token. Always succeeds if JWT is valid
    return get_or_create_user(
        session,
        sub=token["sub"],
        email=token.get("email") or f"{token['sub']}@unknown.local",
        name=token.get("name"),
        role=token.get("role"),
        is_admin=_parse_is_admin(token.get("is_admin")),
    )


# Convert various truthy values to bool
def _parse_is_admin(val) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val == 1
    if isinstance(val, str):
        return val.strip().lower() in {"1", "true", "yes", "y"}
    return False


# Pagination helper (for when we start dealing with the DB more)
@dataclass
class Page:
    limit: int = 20
    cursor: Optional[int] = None


def page(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[int] = Query(
        None, description="id of last item from previous page"
    ),
) -> Page:
    return Page(limit=limit, cursor=cursor)


# Enforce admin access based on DB role/is_admin
def require_admin_db(current_user: User = Depends(get_current_db_user)) -> User:
    allowed_roles = {"admin", "dev", "developer", "superadmin"}
    has_role = current_user.role and current_user.role.lower() in allowed_roles
    has_admin_flag = current_user.is_admin

    if not (has_role or has_admin_flag):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user
