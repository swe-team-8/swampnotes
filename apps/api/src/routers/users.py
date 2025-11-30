from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session
from ..deps import db_session, get_current_db_user
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


# payload (partial updates)
class UserPrefsUpdate(SQLModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    is_profile_public: Optional[bool] = None
    show_email: Optional[bool] = None


# /me GET user endpoint
@router.get("/me")
def get_me(user: User = Depends(get_current_db_user)):
    return {
        "user": {
            "id": user.id,
            "sub": user.sub,
            "email": user.email,
            "name": user.name,
            "display_name": user.display_name,
            "bio": user.bio,
            "is_profile_public": user.is_profile_public,
            "show_email": user.show_email,
            "points": user.points,
        }
    }


# /me PATCH user endpoint
@router.patch("/me")
def update_me(
    payload: UserPrefsUpdate,
    user: User = Depends(get_current_db_user),
    session: Session = Depends(db_session),
):
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "ok": True,
        "user": {
            "display_name": user.display_name,
            "bio": user.bio,
            "is_profile_public": user.is_profile_public,
            "show_email": user.show_email,
        },
    }
