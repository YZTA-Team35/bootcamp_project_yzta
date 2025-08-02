from keras.models import load_model
from pathlib import Path
import os

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "skin_disease_backend_ready.keras"

model = None

def get_model():
    global model
    if model is None:
        # Debug bilgileri
        print(f"🔍 Model path: {MODEL_PATH}")
        print(f"📁 Dosya var mı: {MODEL_PATH.exists()}")
        
        if MODEL_PATH.exists():
            file_size = os.path.getsize(MODEL_PATH) / (1024*1024)
            print(f"📊 Dosya boyutu: {file_size:.1f} MB")
        
        # ML klasöründeki tüm dosyaları listele
        ml_dir = MODEL_PATH.parent
        if ml_dir.exists():
            print(f"📂 ML klasöründeki dosyalar:")
            for file in ml_dir.iterdir():
                if file.is_file():
                    size = os.path.getsize(file) / (1024*1024)
                    print(f"   - {file.name}: {size:.1f} MB")
        
        try:
            model = load_model(MODEL_PATH, compile=False)
            print(f"✅ Model yüklendi - Input shape: {model.input_shape}")
            
            # Model test et
            import numpy as np
            test_input = np.random.random((1, 256, 256, 3))
            test_pred = model.predict(test_input, verbose=0)
            print(f"🧪 Test prediction shape: {test_pred.shape}")
            
        except Exception as e:
            print(f"❌ Model yüklenirken hata oluştu: {e}")
            
            # Alternatif dosya dene
            h5_path = MODEL_PATH.with_suffix('.h5')
            if h5_path.exists():
                print(f"🔄 Alternatif .h5 dosyası deneniyor...")
                try:
                    model = load_model(h5_path, compile=False)
                    print(f"✅ H5 model yüklendi - Input shape: {model.input_shape}")
                except Exception as e2:
                    print(f"❌ H5 model de başarısız: {e2}")
                    model = None
            else:
                model = None
    
    return model