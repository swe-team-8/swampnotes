from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi import APIRouter, Depends
from ..auth_clerk import get_current_user, TokenUser
from fastapi import FastAPI, UploadFile, File, HTTPException
from ..minio_client import create_bucket, upload_to_minio, download_from_minio

router = APIRouter()
BUCKET_NAME = "swampnotes"

@router.post("/upload")
async def upload(file: UploadFile = File(...), current: TokenUser | None = Depends(get_current_user)):
    if not current:
        return {"user": None, "message": "You're not signed in yet."}
    result = upload_to_minio(file, BUCKET_NAME)
    if result:
        return {"message": "Upload successful", "filename": file.filename}
    raise HTTPException(status_code=500, detail="Upload failed")

@router.get("/download/{filename}")
async def download(filename: str, current: TokenUser | None = Depends(get_current_user)):
    if not current:
        return {"user": None, "message": "You're not signed in yet."}
    content = download_from_minio(filename, BUCKET_NAME)
    if content:
        return content
    raise HTTPException(status_code=404, detail="File not found")

