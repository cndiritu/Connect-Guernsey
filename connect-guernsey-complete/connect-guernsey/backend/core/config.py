from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Connect Guernsey"
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:8080"
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480
    ADMIN_EMAIL: str = "admin@connectguernsey.gg"
    ADMIN_PASSWORD: str = "Admin123!"
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "hello@connectguernsey.gg"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
