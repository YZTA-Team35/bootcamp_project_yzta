from keras.models import load_model
from pathlib import Path
import os
import numpy as np

# H5 model dosyasının yolu
MODEL_PATH = Path(__file__).resolve().parent / "skin_disease_reconstructed.h5"

model = None

def get_model():
    global model
    if model is None:
        print(f"🔍 Model path: {MODEL_PATH}")
        if not MODEL_PATH.exists():
            print("❌ Model dosyası bulunamadı.")
            return None
        
        try:
            model = load_model(MODEL_PATH, compile=False)
            print(f"✅ Model yüklendi - Input shape: {model.input_shape}")

            # Test input (doğrulama)
            test_input = np.random.random((1, 256, 256, 3))
            model.predict(test_input, verbose=0)

        except Exception as e:
            print(f"❌ Model yüklenirken hata oluştu: {e}")
            model = None

    return model
