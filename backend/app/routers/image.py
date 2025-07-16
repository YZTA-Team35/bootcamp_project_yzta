from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image_upload import upload_image_to_s3
from app.services.predict import predict_image

router = APIRouter()

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Görseli S3'e yükler ve public URL döner.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Yüklenen dosya bir resim olmalıdır.")

    try:
        url = upload_image_to_s3(file)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Görsel dosyasını alır, modeli çalıştırır ve tahmin sonucunu döner.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Dosya bir resim olmalıdır.")

    try:
        # Dosyayı byte formatında oku
        contents = await file.read()

        # Model tahmini al
        result = predict_image(contents)

        return {"prediction": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin işlemi başarısız: {str(e)}")
