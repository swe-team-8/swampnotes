from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..deps import db_session, require_admin
from ..models import Course
from ..db import create_course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=Course, dependencies=[Depends(require_admin)])
def create_course_endpoint(
    code: str, title: str, school: str, session: Session = Depends(db_session)
):
    # Uses basic duplicate prevention: code+school should be unique enough for now
    # Could be expanded to a proper unique constraint later
    try:
        course = create_course(session, code=code, title=title, school=school)
        return course
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
