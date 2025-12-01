from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel

from ..deps import db_session, require_admin_db
from ..models import Course, User
from ..db import create_course, get_all_courses
from ..models import Note
from typing import List

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    code: str
    title: str
    school: str


@router.post("/", response_model=Course)
def create_course_endpoint(
    course_data: CourseCreate,
    session: Session = Depends(db_session),
    admin: User = Depends(require_admin_db),
):
    # Create a new course (admin only)
    try:
        course = create_course(
            session,
            code=course_data.code,
            title=course_data.title,
            school=course_data.school,
        )
        return course
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Course])
def list_courses(session: Session = Depends(db_session)):
    # Get all courses for directory browsing, public endpoint
    return get_all_courses(session)


@router.get("/{course_id}/notes", response_model=List[Note])
def get_course_notes(
    course_id: int,
    session: Session = Depends(db_session),
):
    # Get all notes for a specific course, public endpoint
    from ..db import search_notes

    return search_notes(session, course_id=course_id, limit=100)
