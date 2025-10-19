import os
import io
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from fastapi.responses import StreamingResponse
from .settings import settings

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    region_name="us-east-1",
    config= Config(signature_version="s3v4",
                   s3={"addressing_style": "path"} if settings.MINIO_FORCE_PATH_STYLE else None,),
)
def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)
def upload_to_minio(file, bucket_name):
    try:
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        return True
    except ClientError as e:
        print(e)
        return False
def download_from_minio(filename, bucket_name):
    try:
        fileobj = io.BytesIO()
        s3.download_fileobj(bucket_name, filename, fileobj)
        fileobj.seek(0)
        return StreamingResponse(fileobj, media_type="application/octet-stream")
    except ClientError as e:
        print(e)
        return None