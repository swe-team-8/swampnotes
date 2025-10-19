from fastapi import APIRouter

# not necessary for this simple router but all routers should import the following line
# from ..deps import db_session, current_user, maybe_user, page

# Health check skeleton
router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}
