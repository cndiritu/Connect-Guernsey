import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("main")

app = FastAPI(title="Connect Guernsey API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    from routers.all_routers import router as all_router
    app.include_router(all_router)
    logger.info("All routers loaded")
except Exception as e:
    logger.error(f"Some routers failed to load: {e}")

@app.get("/")
def root():
    return {"message": "Connect Guernsey API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup():
    logger.info("Starting Connect Guernsey API...")
    try:
        from core.database import get_supabase
        db = get_supabase()
        logger.info("Supabase connected OK")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        return

    # Seed admin using passlib (same as auth.py uses)
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        admin_email = os.getenv("ADMIN_EMAIL", "admin@connectguernsey.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "changeme")

        existing = db.table("admins").select("id").eq("email", admin_email).execute()
        if not existing.data:
            hashed = pwd_context.hash(admin_password)
            db.table("admins").insert({
                "email": admin_email,
                "password_hash": hashed,
                "name": "Admin",
                "is_active": True
            }).execute()
            logger.info(f"Admin account created: {admin_email}")
        else:
            # Always update the hash to ensure it's correct
            hashed = pwd_context.hash(admin_password)
            db.table("admins").update({
                "password_hash": hashed,
                "is_active": True
            }).eq("email", admin_email).execute()
            logger.info(f"Admin password hash refreshed: {admin_email}")
    except Exception as e:
        logger.warning(f"Could not seed admin: {e}")

    # Seed default site settings
    try:
        defaults = {
            "site_name": "Connect Guernsey",
            "site_tagline": "Rooted in Guernsey. Built for everyone.",
            "site_email": "hello@connectguernsey.com",
            "social_linkedin": "",
            "social_facebook": "",
            "launch_date": "2026-05-01"
        }
        for key, value in defaults.items():
            existing = db.table("site_settings").select("id").eq("key", key).execute()
            if not existing.data:
                db.table("site_settings").insert({"key": key, "value": value}).execute()
        logger.info("Default settings seeded")
    except Exception as e:
        logger.warning(f"Could not seed settings: {e}")
