from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Body,
)
from fastapi.responses import StreamingResponse

# Refactored files.py for pure file utility routes and generic file handling rather than note-specific logic
# The note-specific logic now lives in routers/notes.py

from ..deps import (
    get_current_db_user,
    User,
    get_file_from_minio,
    delete_from_minio,
    presign_put,
    presign_get,
)
from ..settings import settings

router = APIRouter(prefix="/files", tags=["files"])
BUCKET_NAME = settings.MINIO_BUCKET


@router.get("/download/{bucket}/{object_key:path}")
async def download_file(
    bucket: str,
    object_key: str,
    current_user: User = Depends(get_current_db_user),
):
    """
    Generic file download from MinIO
    Use /notes/{note_id}/download for note downloads with ownership checks
    """
    content = get_file_from_minio(object_key, bucket)
    if content:
        return StreamingResponse(
            content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{object_key}"'},
        )
    raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{bucket}/{object_key:path}")
async def delete_file(
    bucket: str,
    object_key: str,
    current_user: User = Depends(get_current_db_user),
):
    """
    Generic file deletion from MinIO (admin use)
    For user note deletion, use DELETE /notes/{note_id} instead
    """
    # TODO: Add admin role check
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    res = delete_from_minio(object_key, bucket)
    if res:
        return {"message": "File deleted", "object_key": object_key}
    raise HTTPException(status_code=404, detail="File not found")


@router.post("/presign-upload")
def sign_upload(
    filename: str = Body(..., embed=True),
    content_type: str = Body(..., embed=True),
    bucket: str = Body("notes", embed=True),
    current_user: User = Depends(get_current_db_user),
):
    """
    Generate presigned URL for direct browser → MinIO upload
    Large files/chunks should use this method instead of uploading via API
    """
    # Namespace by user to avoid conflicts
    key = f"users/{current_user.id}/{filename}"
    url = presign_put(key, content_type=content_type, expires=300)
    return {"uploadUrl": url, "objectKey": key, "bucket": bucket, "expiresIn": 300}


@router.post("/presign-download")
def sign_get(
    object_key: str = Body(..., embed=True),
    bucket: str = Body("notes", embed=True),
    current_user: User = Depends(get_current_db_user),
):
    """
    Generate presigned URL for direct browser download from MinIO
    Doesn't check ownership, use /notes/{note_id}/download for that
    """
    url = presign_get(object_key, expires=300, bucket_name=bucket)
    return {"url": url, "expiresIn": 300}
