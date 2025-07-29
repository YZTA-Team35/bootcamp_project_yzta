from keras.models import load_model
from keras.saving import enable_unsafe_deserialization  # 👈 Eklendi
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "best_model_epoch_01_val_acc_0.7063.keras"

model = None

def get_model():
    global model
    if model is None:
        enable_unsafe_deserialization()  # 👈 değiştirsen iyi olur
        model = load_model(MODEL_PATH)
    return model

"""
from keras.models import load_model
from pathlib import Path

# Yeni model yolu (yeni uzantıyla)
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "best_model_epoch_01_val_acc_0.7063.keras"

model = None

def get_model():
    global modela
    if model is None:
        model = load_model(MODEL_PATH)
    return model
"""