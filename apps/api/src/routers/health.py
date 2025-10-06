from fastapi import APIRouter

# Health check skeleton
router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}
