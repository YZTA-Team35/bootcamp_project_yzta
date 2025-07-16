import google.generativeai as genai
from config.settings import settings

# Gemini API anahtarını ayarla
genai.configure(api_key=settings.GEMINI_API_KEY)

# Gemini 2.0 Flash modelini kullan
model = genai.GenerativeModel("gemini-2.0-flash")

def explain_prediction_with_gemini(predicted_class: str) -> str:
    """
    Tahmin edilen cilt hastalığını Gemini'ye sorarak açıklama alır.
    """
    prompt = (
        f"Bir kullanıcıdan gelen cilt görüntüsü, bir yapay zeka modeli tarafından '{predicted_class}' olarak tahmin edildi. "
        f"Lütfen bu hastalığı sade ve anlaşılır bir dille açıkla. Neden oluşur, nasıl belirtiler verir ve genelde nasıl tedavi edilir? "
        f"Açıklama 5-6 cümleyi geçmesin. Korkutucu dil kullanma, bilgilendirici ve sade olsun."
    )

    response = model.generate_content(prompt)
    return response.text.strip()
