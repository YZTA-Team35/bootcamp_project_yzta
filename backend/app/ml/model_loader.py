from keras.models import load_model
from pathlib import Path
import os

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "skin_disease_backend_ready.keras"

model = None

def get_model():
    global model
    if model is None:
        try:
            model = load_model(MODEL_PATH, compile=False)
            print(f"✅ Model yüklendi - Input shape: {model.input_shape}")
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            model = None
    return model
