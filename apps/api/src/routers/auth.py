from __future__ import annotations
from fastapi import APIRouter, Depends
from ..deps import optional_user, require_user, TokenUser

# endpoint routing
router = APIRouter(prefix="/auth", tags=["auth"])


# simple auth test endpoint (removed email authentication since Clerk handles that)
@router.get("/me")
async def me(current: TokenUser | None = Depends(optional_user)):
    print(current)
    if not current:
        return {"user": None, "message": "You're not signed in yet."}
    return {
        "user": {
            "sub": current.get("sub"),
            "name": current.get("name"),
            "email": current.get("email"),
            "username": current.get("username"),
        },
        "message": "Signed in.",
    }


@router.get("/whoami")
async def whoami(current: TokenUser = Depends(require_user)):
    return {
        "sub": current["sub"],
        "email": current.get("email"),
        "username": current.get("username"),
    }
