from keras.models import load_model
import numpy as np
from PIL import Image
import io
from pathlib import Path
import tensorflow as tf

# ✅ Model dosyasının doğru yolunu belirtiyoruz
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "best_efficientnet_finetuned.h5"

# ✅ Modeli yalnızca bir kez yüklemek için başlangıçta yüklüyoruz
model = load_model(MODEL_PATH)

# ✅ Tahmin sınıflarını burada belirt (örnek)
# Bunları modelini eğitirken kullandığın class sıralamasına göre yaz
CLASS_NAMES = [
    "Acne", "Eczema", "Psoriasis", "Rosacea", "Melanoma"
    # ← Buraya kendi modelinin class_labels'ını yazmalısın
]

def predict_image(image_bytes: bytes) -> str:
    """
    S3'ten gelen resmi model ile sınıflandırır.
    """
    try:
        # ✅ Görseli oku ve modele uygun şekilde yeniden boyutlandır
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))  # EfficientNet genelde 224x224 alır, emin ol
        image_array = np.array(image) / 255.0  # normalize et
        image_array = np.expand_dims(image_array, axis=0)  # batch boyutu ekle (1, 224, 224, 3)

        # ✅ Modelle tahmin yap
        predictions = model.predict(image_array)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]

        return predicted_class

    except Exception as e:
        return f"Prediction failed: {str(e)}"
