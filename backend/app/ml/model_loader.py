from keras.models import load_model
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "best_model_epoch_01_val_acc_0.7063.keras"

model = None

def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH, compile=False)
    return model
