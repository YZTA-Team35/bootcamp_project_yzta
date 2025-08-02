from keras.models import load_model
from pathlib import Path

MODEL_PATH = Path(_file_).resolve().parent.parent / "ml" / "skin_disease_rgb_final.keras"

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
