from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form, Depends
from fastapi.responses import Response
from sqlmodel import Session, select, func
from typing import Optional, List
import uuid
import logging

from ..deps import (
    db_session,
    get_current_db_user,
    User,
    Note,
    Course,
    Purchase,
    create_note,
    search_notes,
    get_user_purchased_notes,
    get_user_uploaded_notes,
    create_purchase,
    has_purchased_note,
    upload_bytes_to_minio,
    get_file_from_minio,
    delete_from_minio,
)

router = APIRouter(prefix="/notes", tags=["notes"])
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=Note)
async def upload_note(
    file: UploadFile = File(...),
    title: str = Form(...),
    course_id: str = Form(...),
    course_name: str = Form(...),
    semester: str = Form(...),
    description: Optional[str] = Form(None),
    price: str = Form("100"),
    is_free: str = Form("false"),
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    # Upload a new note (authenticated users only)
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("application/pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Validate and convert course_id
        try:
            course_id_int = int(course_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid course ID format")

        # Parse price and is_free
        try:
            price_int = int(price)
            is_free_bool = is_free.lower() in ("true", "1", "yes")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid price format")

        # Verify course exists in database
        course = session.get(Course, course_id_int)
        if not course:
            logger.error(f"Course {course_id_int} not found in database")
            raise HTTPException(
                status_code=400,
                detail=f"Course with ID {course_id_int} does not exist. Please select a valid course.",
            )

        # Generate unique object key
        file_ext = file.filename.split(".")[-1] if "." in file.filename else "pdf"
        object_key = f"{uuid.uuid4()}.{file_ext}"

        # Upload to MinIO first
        file_data = await file.read()
        success = upload_bytes_to_minio(
            file_data, object_key, "notes", file.content_type
        )

        if not success:
            logger.error(f"Failed to upload {object_key} to MinIO")
            raise HTTPException(
                status_code=500, detail="Failed to upload file to storage"
            )

        logger.info(f"Successfully uploaded {object_key} to MinIO")

        # Create note in database
        try:
            note = create_note(
                session,
                author_id=current_user.id,
                course_id=course_id_int,
                title=title,
                course_name=course_name,
                semester=semester,
                description=description,
                object_key=object_key,
                file_type=file.content_type,
                price=price_int,
                is_free=is_free_bool,
            )
            logger.info(f"Successfully created note {note.id} in database")
            return note
        except Exception as db_error:
            logger.error(
                f"Database error creating note: {str(db_error)}", exc_info=True
            )
            # Clean up MinIO upload if DB operation fails
            delete_from_minio(object_key, "notes")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save note to database: {str(db_error)}",
            )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during upload: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/search", response_model=List[Note])
def search_notes_endpoint(
    query: Optional[str] = Query(None, description="Search term"),
    course_id: Optional[int] = Query(None),
    semester: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(db_session),
):
    # Search notes with filters, public endpoint
    return search_notes(
        session,
        query=query,
        course_id=course_id,
        semester=semester,
        limit=limit,
        offset=offset,
    )


@router.get("/library", response_model=List[Note])
def get_library(
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    """Get user's purchased notes (Library tab)."""
    return get_user_purchased_notes(session, user_id=current_user.id)


@router.get("/uploaded", response_model=List[Note])
def get_uploaded(
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    """Get user's uploaded notes (Uploaded tab)."""
    return get_user_uploaded_notes(session, user_id=current_user.id)


@router.get("/debug/stats")
def get_note_stats(session: Session = Depends(db_session)):
    # Debug endpoint to check note count in database
    total_notes = session.exec(select(func.count(Note.id))).one()
    total_courses = session.exec(select(func.count(Course.id))).one()

    # Get sample notes
    recent_notes = session.exec(
        select(Note).order_by(Note.created_at.desc()).limit(5)
    ).all()

    return {
        "total_notes": total_notes,
        "total_courses": total_courses,
        "recent_notes": [
            {
                "id": n.id,
                "title": n.title,
                "course_id": n.course_id,
                "author_id": n.author_id,
                "created_at": n.created_at,
            }
            for n in recent_notes
        ],
    }


@router.get("/{note_id}", response_model=Note)
def get_note_by_id(note_id: int, session: Session = Depends(db_session)):
    # Get a single note by ID, public endpoint
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Increment view count
    note.views = (note.views or 0) + 1
    session.add(note)
    session.commit()
    session.refresh(note)

    return note


@router.post("/{note_id}/purchase", response_model=Purchase)
def purchase_note_endpoint(
    note_id: int,
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    # Purchase a note with points
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Free notes bypass payment
    price = 0 if note.is_free else note.price

    try:
        purchase = create_purchase(
            session, user_id=current_user.id, note_id=note_id, price=price
        )
        return purchase
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{note_id}/owned")
def check_ownership(
    note_id: int,
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    # Check if current user owns this note
    owned = has_purchased_note(session, user_id=current_user.id, note_id=note_id)
    is_author = False
    note = session.get(Note, note_id)
    if note:
        is_author = note.author_id == current_user.id

    return {
        "owned": owned or is_author,
        "is_author": is_author,
        "can_download": owned or is_author,
    }


@router.get("/{note_id}/download")
async def download_note(
    note_id: int,
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_db_user),
):
    """Download a note file (requires ownership)"""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Check ownership
    is_owner = note.author_id == current_user.id
    has_purchased_note_flag = has_purchased_note(
        session, user_id=current_user.id, note_id=note_id
    )

    if not (is_owner or has_purchased_note_flag or note.is_free):
        raise HTTPException(
            status_code=403, detail="You must purchase this note to download it"
        )

    if not note.object_key:
        raise HTTPException(status_code=404, detail="File not found")

    # Get file from MinIO
    try:
        file_data = get_file_from_minio(note.object_key, "notes")

        if not file_data:
            raise HTTPException(
                status_code=500, detail="Failed to retrieve file from storage"
            )

        # Increment download count
        note.downloads = (note.downloads or 0) + 1
        session.add(note)
        session.commit()

        # Read the entire stream into memory
        content = file_data.read()

        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{note.title}.pdf"',
                "Content-Length": str(len(content)),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to download file: {str(e)}"
        )
