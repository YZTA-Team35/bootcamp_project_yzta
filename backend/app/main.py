# NOT: CORS (Cross-Origin Resource Sharing) middleware'i frontend ile backend farklı domain/portlarda çalışırken
# API isteklerinin engellenmemesi için EKLENMİŞTİR. Şu anda sadece local geliştirme (localhost) ve Railway backend için izin verilmiştir.
# Canlıya alırken sadece güvenli domainlere izin verilmelidir!

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import Base, engine
from app.routers import auth, image
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI()

# CORS middleware EKLENDİ
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://bootcamp-project-yzta-r264.vercel.app"    ],  # Sadece local ve vercel frontend izinli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(image.router, prefix="/images")

