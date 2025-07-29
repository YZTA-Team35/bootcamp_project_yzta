import boto3
from uuid import uuid4
from fastapi import UploadFile
from config.settings import settings

def upload_image_to_s3(file: UploadFile) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    file_extension = file.filename.split(".")[-1]
    file_key = f"{uuid4()}.{file_extension}"  # benzersiz isim

    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET_NAME,
        file_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    # Public URL üret
    public_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
    return public_url
