from fastapi import FastAPI
from app.database.session import Base, engine
from app.routers import auth, image

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(image.router, prefix="/images")