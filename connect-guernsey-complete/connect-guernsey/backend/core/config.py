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

    # Lowercase aliases so all routers work
    @property
    def admin_email(self): return self.ADMIN_EMAIL
    @property
    def admin_password(self): return self.ADMIN_PASSWORD
    @property
    def supabase_url(self): return self.SUPABASE_URL
    @property
    def supabase_service_key(self): return self.SUPABASE_SERVICE_KEY
    @property
    def jwt_secret(self): return self.JWT_SECRET
    @property
    def jwt_algorithm(self): return self.JWT_ALGORITHM
    @property
    def resend_api_key(self): return self.RESEND_API_KEY
    @property
    def email_from(self): return self.EMAIL_FROM
    @property
    def frontend_url(self): return self.FRONTEND_URL

settings = Settings()

def get_settings() -> Settings:
    return settings

def get_client():
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
