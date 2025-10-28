from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, Field  # noqa: F401
from ..deps import db_session, require_user, TokenUser
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


# payload (partial updates)
class UserPrefsUpdate(SQLModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    is_profile_public: Optional[bool] = None
    show_email: Optional[bool] = None


def ensure_user(sess: Session, tok: TokenUser) -> User:
    # Resolve user by: clerk 'sub'ject -> fallback to postgres (email) -> create if both fail
    user = sess.exec(select(User).where(User.sub == tok["sub"])).first()
    if not user and tok.get("email"):
        user = sess.exec(select(User).where(User.email == tok["email"])).first()
    if not user:
        user = User(
            sub=tok["sub"],
            email=tok.get("email") or f"{tok['sub']}@unknown.local",
            name=tok.get("name"),
        )
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    if not user.sub:
        user.sub = tok["sub"]
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    return user


# /me GET user endpoint
@router.get("/me")
def get_me(sess: Session = Depends(db_session), tok: TokenUser = Depends(require_user)):
    u = ensure_user(sess, tok)
    return {
        "user": {
            "id": u.id,
            "sub": u.sub,
            "email": u.email,
            "name": u.name,
            "display_name": u.display_name,
            "bio": u.bio,
            "is_profile_public": u.is_profile_public,
            "show_email": u.show_email,
        }
    }


# /me PATCH user endpoint
@router.patch("/me")
def update_me(
    payload: UserPrefsUpdate,
    sess: Session = Depends(db_session),
    tok: TokenUser = Depends(require_user),
):
    u = ensure_user(sess, tok)
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(u, k, v)
    sess.add(u)
    sess.commit()
    sess.refresh(u)
    return {
        "ok": True,
        "user": {
            "display_name": u.display_name,
            "bio": u.bio,
            "is_profile_public": u.is_profile_public,
            "show_email": u.show_email,
        },
    }
