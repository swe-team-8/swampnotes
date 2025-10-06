from fastapi import APIRouter, Depends, HTTPException  # noqa: F401
from starlette.requests import Request

# Skeleton authentication provider code
router = APIRouter()


@router.get("/auth/me")
def me(request: Request):
    # Replace this with real JWT verification later
    return {"user": None, "onboardingRequired": True}
