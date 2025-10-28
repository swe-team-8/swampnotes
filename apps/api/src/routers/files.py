from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body

from ..deps import require_user
from ..auth_clerk import TokenUser
from ..settings import settings
from ..minio_client import (
    upload_to_minio,
    download_from_minio,
    presign_put,
    presign_get,
)

router = APIRouter(prefix="/uploads", tags=["uploads"])
BUCKET_NAME = settings.MINIO_BUCKET


# Proxy uploads (for dev purposes)
@router.post("/upload")
async def upload_proxy(
    file: UploadFile = File(...),
    user: TokenUser = Depends(require_user),
):
    ok = upload_to_minio(file, BUCKET_NAME)
    if ok:
        return {"message": "Upload successful", "filename": file.filename}
    raise HTTPException(status_code=500, detail="Upload failed")


# Proxy downloads (for dev purposes)
@router.get("/download/{filename}")
async def download_proxy(
    filename: str,
    user: TokenUser = Depends(require_user),
):
    content = download_from_minio(filename, BUCKET_NAME)
    if content:
        return content
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
