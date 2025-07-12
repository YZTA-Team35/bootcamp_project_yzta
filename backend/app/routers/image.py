from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image_upload import upload_image_to_s3

router = APIRouter()

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        url = upload_image_to_s3(file)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
