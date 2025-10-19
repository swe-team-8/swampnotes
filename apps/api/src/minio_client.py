import io
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from fastapi.responses import StreamingResponse
from .settings import settings


# add extension to MINIO_ENDPOINT if necessary (less strict)
def _endpoint_base() -> str:
    e = settings.MINIO_ENDPOINT
    return e if e.startswith("http://") or e.startswith("https://") else f"http://{e}"


s3 = boto3.client(
    "s3",
    endpoint_url=_endpoint_base(),
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    region_name="us-east-1",
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"} if settings.MINIO_FORCE_PATH_STYLE else None,
    ),
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


# Presign URLs (grants temp access to a private object in the storage bucket)
def presign_put(key: str, content_type: str, expires: int = 300) -> str:
    return s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.MINIO_BUCKET,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires,
    )


def presign_get(key: str, expires: int = 300) -> str:
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.MINIO_BUCKET, "Key": key},
        ExpiresIn=expires,
    )
