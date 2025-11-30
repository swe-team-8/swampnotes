from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session

from ..deps import db_session, get_current_db_user
from ..settings import settings
from ..models import Note, User
from ..db import create_note
from ..minio_client import upload_to_minio

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/upload", response_model=Note)
async def upload_note(
    file: UploadFile,
    title: str,
    course_id: int,
    course_name: str,
    semester: str,
    description: Optional[str] = None,
    user: User = Depends(get_current_db_user),
    session: Session = Depends(db_session),
):
    # Upload file to MinIO and use filename as object key
    object_key = file.filename
    ok = upload_to_minio(file, bucket_name=settings.MINIO_BUCKET)
    if not ok:
        raise HTTPException(status_code=500, detail="MinIO upload failed")

    try:
        note = create_note(
            session,
            author_id=user.id,
            course_id=course_id,
            title=title,
            course_name=course_name,
            semester=semester,
            description=description,
            object_key=object_key,
            file_type=file.content_type,
        )
        return note
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
