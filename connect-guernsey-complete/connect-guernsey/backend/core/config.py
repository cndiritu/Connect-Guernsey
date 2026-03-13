import os

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@connectguernsey.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "changeme")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "hello@connectguernsey.com")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://connectguernsey.com")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

settings = Settings()
