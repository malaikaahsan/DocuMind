import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "DocuMind")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    MONGO_URI: str = os.getenv("MONGO_URI", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "documind")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "")


settings = Settings()