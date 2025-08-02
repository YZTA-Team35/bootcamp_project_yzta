from keras.models import load_model
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "SkinDiseaseWeightsPre1.h5"

model = None

def get_model():
    global model
    if model is None:
        try:
            model = load_model(MODEL_PATH, compile=False)  # lambda varsa dikkatli ol!
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            model = None
    return model
