from keras.models import load_model
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "SkinDiseaseWeightsPre1.h5"  # .h5 dosyanın adı buysa

model = None

def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH, compile=False)  # compile=False daha güvenli ve hızlı yükler
    return model
