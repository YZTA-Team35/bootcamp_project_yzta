from keras.models import load_model
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "skin_disease_complete_model.h5"

model = None

def get_model():
    global model
    if model is None:
        # Önce .keras dene
        keras_path = Path(__file__).resolve().parent.parent / "ml" / "skin_disease_complete_model.keras"
        h5_path = Path(__file__).resolve().parent.parent / "ml" / "skin_disease_complete_model.h5"
        
        for path in [keras_path, h5_path]:
            try:
                model = load_model(path, compile=False)
                print(f"✅ Model yüklendi: {path.name} - Input shape: {model.input_shape}")
                break
            except Exception as e:
                print(f"❌ {path.name} yüklenemedi: {e}")
                continue
            return model
        
