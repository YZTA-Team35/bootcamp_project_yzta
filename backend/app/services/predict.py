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
     # Görseli PIL ile yükle
    image = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
    img_array = np.array(image) / 255.0  # normalize et
    img_array = np.expand_dims(img_array, axis=0)

    # Tahmin yap
    predictions = model.predict(img_array)

    # En yüksek olasılığı ve indeksini al
    predicted_index = np.argmax(predictions)
    confidence = float(predictions[0][predicted_index])

    # Sınıf isimlerini burada belirt
    class_names = ["acne", "eczema", "psoriasis", "melanoma"]  # Örnek olarak
    predicted_class = class_names[predicted_index]

    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2)  # Yüzde olarak (%)
    }