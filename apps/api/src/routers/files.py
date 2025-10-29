from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body

from .. import minio_client  # noqa: F401
from ..deps import require_user
from ..auth_clerk import TokenUser
from ..settings import settings
from ..minio_client import (
    upload_to_minio,
    download_from_minio,
    delete_from_minio,
    presign_put,
    presign_get,
)

router = APIRouter(prefix="/notes", tags=["notes"])
BUCKET_NAME = settings.MINIO_BUCKET

# Constants
FILE_SIZE_LIMIT = 1e8  # (In Bytes, 1/10 of a gigabyte)
ACCEPTABLE_TYPES = ["application/pdf", "text/plain"]


# Proxy uploads (for dev purposes)
@router.post("/upload")
async def upload_proxy(
    file: UploadFile = File(...),
    user: TokenUser = Depends(require_user),
):
    file.filename = f"Notes/{user.get('username')}/{file.filename}"

    # File Restrictions
    if file.size > FILE_SIZE_LIMIT:
        raise HTTPException(status_code=413, detail="File size exceeds limit")
    if file.content_type not in ACCEPTABLE_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    # Check if the file already exists
    is_in_bucket = download_from_minio(
        file.filename, BUCKET_NAME
    )  # TODO: Replace this with something more efficient later on
    if is_in_bucket:
        raise HTTPException(
            status_code=409, detail="File with the same name already exists"
        )
    ok = upload_to_minio(file, BUCKET_NAME)
    if ok:
        return {"message": "Upload successful", "filename": file.filename}
    raise HTTPException(status_code=500, detail="Upload failed")


# Proxy downloads (for dev purposes)
@router.get("/download/{author}/{filename}")
async def download_proxy(
    author: str,
    filename: str,
    user: TokenUser = Depends(require_user),
):
    filename = f"Notes/{author}/{filename}"
    content = download_from_minio(filename, BUCKET_NAME)
    if content:
        return content
    raise HTTPException(status_code=404, detail="File not found")


@router.get("/delete/{filename}")
async def delete(filename: str, user: TokenUser = Depends(require_user)):
    filename = f"Notes/{user.get('username')}/{filename}"
    res = delete_from_minio(filename, BUCKET_NAME)
    if res:
        return {"message": "File deleted"}
    raise HTTPException(status_code=404, detail="File not found")


# Presigned uploads (for browser -> minIO uploads)
@router.post("/uploads/sign")
def sign_upload(
    filename: str = Body(..., embed=True),
    content_type: str = Body(..., embed=True),
    user: TokenUser = Depends(require_user),
):
    # Filter by user to avoid conflicts when sharing a bucket
    key = f"users/{user['sub']}/{filename}"
    url = presign_put(key, content_type=content_type, expires=300)
    return {"uploadUrl": url, "objectKey": key}


# Presigned downloads
@router.get("/uploads/sign-get")
def sign_get(
    key: str,
    user: TokenUser = Depends(require_user),
):
    # Validate ownership before signing (optional)
    url = presign_get(key, expires=300)
    return {"url": url}
