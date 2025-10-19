from fastapi import APIRouter, Depends
from ..auth_clerk import get_current_user, TokenUser
from ..settings import settings

router = APIRouter()


@router.get("/auth/me")
async def me(current: TokenUser | None = Depends(get_current_user)):
    if not current:
        return {"user": None, "message": "You're not signed in yet."}

    # restrict to school domains
    domains = settings.ALLOWED_EMAIL_DOMAINS or []
    if (
        current.get("email")
        and domains
        and not any(current["email"].endswith(f"@{d}") for d in domains)
    ):
        return {"user": None, "message": "Email domain not allowed."}

    # Keep it simple for testing purposes: do NOT write to DB yet (requires password)
    return {
        "user": {
            "sub": current.get("sub"),
            "email": current.get("email"),
        },
        "message": "Signed in.",
    }
