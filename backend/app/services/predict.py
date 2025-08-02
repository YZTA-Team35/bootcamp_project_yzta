from PIL import Image
import numpy as np
import io
from app.ml.model_loader import get_model
from app.services.explanation import explain_prediction_with_gemini

CLASS_NAMES = [
    'Actinic keratosis', 'Basal cell carcinoma', 'Benign keratosis', 
    'Dermatofibroma', 'Melanocytic nevus', 'Melanoma', 
    'Squamous cell carcinoma', 'Vascular lesion'
]

def predict_image(image_bytes: bytes) -> dict:
    """
    Görseli işler, modelin beklediği kanal yapısına göre dönüştürür, tahmin yapar ve Gemini açıklamasıyla birlikte döner.
    """
    model = get_model()
    if model is None:
        raise RuntimeError("Model yüklenemedi.")

    # Modelin beklediği input shape (None, 256, 256, 3) veya (None, 256, 256, 1)
    input_shape = model.input_shape[1:]  # (256, 256, 3) veya (256, 256, 1)
    expected_channels = input_shape[-1]

    # Görseli uygun kanala göre oku
    if expected_channels == 1:
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
    else:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Boyutlandır ve normalize et
    image = image.resize(input_shape[:2])
    img_array = np.array(image) / 255.0

    # Kanal ekseni ekle (grayscale için)
    if expected_channels == 1 and img_array.ndim == 2:
        img_array = np.expand_dims(img_array, axis=-1)

    img_array = np.expand_dims(img_array, axis=0)  # (1, H, W, C)

    # Tahmin
    predictions = model.predict(img_array)
    predicted_index = int(np.argmax(predictions))
    confidence = float(predictions[0][predicted_index])
    predicted_class = CLASS_NAMES[predicted_index]

    explanation = explain_prediction_with_gemini(predicted_class)

    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2),
        "explanation": explanation
    }
