# app/services/storage_service.py
import boto3
from botocore.client import Config
from app.core.config import settings


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name=settings.S3_REGION,
    )


def upload_file(file_bytes: bytes, s3_key: str, content_type: str = "application/pdf") -> str:
    """
    Upload file to S3/MinIO.
    Returns the s3_key on success.
    """
    client = get_s3_client()
    client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=s3_key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return s3_key


def get_presigned_url(s3_key: str, expires_in: int = 3600) -> str:
    """
    Generate a presigned URL for temporary file access.
    expires_in = seconds (default 1 hour)
    """
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": s3_key},
        ExpiresIn=expires_in,
    )


def delete_file(s3_key: str) -> None:
    client = get_s3_client()
    client.delete_object(Bucket=settings.S3_BUCKET, Key=s3_key)