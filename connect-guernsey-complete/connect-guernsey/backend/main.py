import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Connect Guernsey API...")
    try:
        from core.database import get_client
        from core.config import settings
        db = get_client()
        logger.info("Supabase connected OK")
        # Seed default admin
        try:
            from core.auth import hash_password
            existing = db.table("admins").select("id").eq("email", settings.admin_email).execute()
            if not existing.data:
                db.table("admins").insert({
                    "name": "Admin",
                    "email": settings.admin_email,
                    "password_hash": hash_password(settings.admin_password),
                    "is_active": True
                }).execute()
                logger.info(f"Default admin created: {settings.admin_email}")
            else:
                logger.info("Admin already exists")
        except Exception as e:
            logger.warning(f"Could not seed admin: {e}")
        # Seed default settings
        try:
            defaults = [
                ("site_name", "Connect Guernsey"),
                ("site_tagline", "Rooted in Guernsey. Built for everyone."),
                ("site_email", "hello@connectguernsey.com"),
                ("social_linkedin", "#"),
                ("social_facebook", "#"),
                ("launch_date", "May 2026"),
            ]
            for key, value in defaults:
                existing = db.table("site_settings").select("id").eq("key", key).execute()
                if not existing.data:
                    db.table("site_settings").insert({"key": key, "value": value}).execute()
            logger.info("Default settings seeded")
        except Exception as e:
            logger.warning(f"Could not seed settings: {e}")
    except Exception as e:
        logger.error(f"Startup error: {e}")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Connect Guernsey API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
frontend_url = os.getenv("FRONTEND_URL", "https://connectguernsey.com")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "https://connectguernsey.netlify.app",
        "https://connectguernsey.com",
        "https://www.connectguernsey.com",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Connect Guernsey API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Include routers safely
try:
    from routers.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    logger.info("Auth router loaded")
except Exception as e:
    logger.error(f"Auth router failed: {e}")

try:
    from routers.members import router as members_router
    app.include_router(members_router, prefix="/api/members", tags=["members"])
    logger.info("Members router loaded")
except Exception as e:
    logger.error(f"Members router failed: {e}")

try:
    from routers.events import router as events_router
    app.include_router(events_router, prefix="/api/events", tags=["events"])
    logger.info("Events router loaded")
except Exception as e:
    logger.error(f"Events router failed: {e}")

try:
    from routers.blog import router as blog_router
    app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
    logger.info("Blog router loaded")
except Exception as e:
    logger.error(f"Blog router failed: {e}")

try:
    from routers.all_routers import (
        team_router, gallery_router, partners_router,
        enquiries_router, content_router, settings_router,
        admins_router, media_router
    )
    app.include_router(team_router, prefix="/api/team", tags=["team"])
    app.include_router(gallery_router, prefix="/api/gallery", tags=["gallery"])
    app.include_router(partners_router, prefix="/api/partners", tags=["partners"])
    app.include_router(enquiries_router, prefix="/api/enquiries", tags=["enquiries"])
    app.include_router(content_router, prefix="/api/content", tags=["content"])
    app.include_router(settings_router, prefix="/api/settings", tags=["settings"])
    app.include_router(admins_router, prefix="/api/admins", tags=["admins"])
    app.include_router(media_router, prefix="/api/media", tags=["media"])
    logger.info("All routers loaded")
except Exception as e:
    logger.error(f"Some routers failed to load: {e}")
