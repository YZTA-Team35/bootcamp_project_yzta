from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    GEMINI_API_KEY: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"  # backend/.env
        env_file_encoding = "utf-8"

settings = Settings()
