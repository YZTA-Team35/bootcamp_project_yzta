from fastapi import FastAPI
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
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://bootcampprojectyzta-production.up.railway.app"
    ],  # Sadece local ve Railway backend izinli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(image.router, prefix="/images")

