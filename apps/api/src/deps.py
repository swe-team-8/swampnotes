from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from collections.abc import Generator

from fastapi import Depends, Query  # noqa: F401
from sqlmodel import Session

from .db import get_session, get_or_create_user
from .models import User

# This file gives us a single place to import dependencies when creating/developing routers
# i.e. can cleanly give a router access to auth + jwt/database as necessary w/o messy imports

# Re-export names from .auth
from .auth import (
    require_user,  # noqa: F401
    optional_user,  # noqa: F401
    require_admin,  # noqa: F401
    TokenUser,  # noqa: F401
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
    )


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
