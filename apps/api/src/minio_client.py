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

# Export s3 client as minio_client for compatibility
minio_client = s3


def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)


def upload_to_minio(file, filename, bucket_name):
    try:
        s3.upload_fileobj(io.BytesIO(file), bucket_name, filename)
        return True
    except ClientError as e:
        print(e)
        return False


def upload_bytes_to_minio(
    data: bytes, filename: str, bucket_name: str, content_type: str = "application/pdf"
) -> bool:
    # Upload bytes directly to MinIO
    try:
        s3.upload_fileobj(
            io.BytesIO(data),
            bucket_name,
            filename,
            ExtraArgs={"ContentType": content_type},
        )
        return True
    except ClientError as e:
        print(e)
        return False


def delete_from_minio(filename, bucket_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=filename)
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


def get_file_from_minio(filename: str, bucket_name: str) -> io.BytesIO:
    # Get file as BytesIO object (for custom streaming)
    try:
        fileobj = io.BytesIO()
        s3.download_fileobj(bucket_name, filename, fileobj)
        fileobj.seek(0)
        return fileobj
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


# Ensure notes bucket exists on startup
try:
    create_bucket("notes")
except Exception as e:
    print(f"Warning: Could not create/verify notes bucket: {e}")
