from PIL import Image
import numpy as np
import io
from app.ml.model_loader import get_model
from app.services.explanation import explain_prediction_with_gemini

# Eğitimdeki sınıf isimleri
CLASS_NAMES = ['Actinic keratosis', 'Basal cell carcinoma', 'Benign keratosis', 'Dermatofibroma', 'Melanocytic nevus', 'Melanoma', 'Squamous cell carcinoma', 'Vascular lesion']

def predict_image(image_bytes: bytes) -> dict:
    """
    Görseli işler, modelle tahmin yapar, sonucu ve Gemini açıklamasını döner.
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("L")  # Grayscale
    image = image.resize((256, 256))

    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=-1)  # (256, 256, 1)
    img_array = np.expand_dims(img_array, axis=0)   # (1, 256, 256, 1)

    model = get_model()
    if model is None:
        raise RuntimeError("Model yüklenemedi.")

    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions)
    confidence = float(predictions[0][predicted_index])
    predicted_class = CLASS_NAMES[predicted_index]

    explanation = explain_prediction_with_gemini(predicted_class)

    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2),
        "explanation": explanation
    }
