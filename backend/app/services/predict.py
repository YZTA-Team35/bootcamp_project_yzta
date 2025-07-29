from keras.models import load_model
import numpy as np
from PIL import Image
import io
from pathlib import Path
from app.services.explanation import explain_prediction_with_gemini

# Model yolunu belirle
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "best_efficientnet_finetuned.h5"
model = load_model(MODEL_PATH)

# Sınıf etiketleri — modeline göre güncelle
CLASS_NAMES = ["acne", "eczema", "psoriasis", "melanoma"]

def predict_image(image_bytes: bytes) -> dict:
    """
    Görseli RGB olarak açar, yeniden boyutlandırır, normalize eder,
    modeli kullanarak tahmin yapar ve Gemini ile açıklama üretir.
    """
    # 🔁 Görseli oku ve RGB'ye dönüştür
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 🔁 Resize et
    image = image.resize((224, 224))

    # 🔁 Normalize ve batch dimension ekle
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)

    # 🔁 Model tahmini
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = float(predictions[0][predicted_index])
    predicted_class = CLASS_NAMES[predicted_index]

    # 🔁 Gemini ile açıklama al
    explanation = explain_prediction_with_gemini(predicted_class)

    # 🔁 Sonucu döndür
    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2),
        "explanation": explain_prediction_with_gemini(predicted_class)
}
