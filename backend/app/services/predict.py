from PIL import Image
import numpy as np
import io
from app.ml.model_loader import get_model
from app.services.explanation import explain_prediction_with_gemini

# Eğitimdeki sınıf isimleri
CLASS_NAMES = [
    "Acne and Rosacea Photos",
    "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions",
    "Atopic Dermatitis Photos",
    "Bullous Disease Photos",
    "Cellulitis Impetigo and other Bacterial Infections",
    "Eczema Photos",
    "Exanthems and Drug Eruptions",
    "Herpes HPV and other STDs Photos",
    "Light Diseases and Disorders of Pigmentation",
    "Lupus and other Connective Tissue diseases",
    "Melanoma Skin Cancer Nevi and Moles",
    "Poison Ivy Photos and other Contact Dermatitis",
    "Psoriasis pictures Lichen Planus and related diseases",
    "Seborrheic Keratoses and other Benign Tumors",
    "Systemic Disease",
    "Tinea Ringworm Candidiasis and other Fungal Infections",
    "Urticaria Hives",
    "Vascular Tumors",
    "Vasculitis Photos",
    "Warts Molluscum and other Viral Infections"
]

def predict_image(image_bytes: bytes) -> dict:
    """
    Görseli işler, modelle tahmin yapar, sonucu ve Gemini açıklamasını döner.
    """
    # Görseli oku ve dönüştür
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    # Normalize ve batch boyutu ekle
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)

    # Modeli al ve tahmin yap
    model = get_model()
    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions)
    confidence = float(predictions[0][predicted_index])
    predicted_class = CLASS_NAMES[predicted_index]

    # Gemini'den açıklama al
    explanation = explain_prediction_with_gemini(predicted_class)

    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2),
        "explanation": explanation
    }
