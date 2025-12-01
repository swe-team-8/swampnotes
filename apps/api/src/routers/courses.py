from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..deps import db_session, require_admin_db
from ..models import Course, User
from ..db import create_course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=Course)
def create_course_endpoint(
    code: str,
    title: str,
    school: str,
    session: Session = Depends(db_session),
    admin: User = Depends(require_admin_db),  # DB-backed admin check
):
    try:
        course = create_course(session, code=code, title=title, school=school)
        return course
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
