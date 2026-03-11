from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import get_settings
from core.database import get_supabase
from core.auth import hash_password
from routers.auth import router as auth_router
from routers.members import router as members_router
from routers.events import router as events_router
from routers.blog import router as blog_router
from routers.all_routers import (team_router, gallery_router, partners_router,
    enquiries_router, content_router, settings_router, admins_router, media_router)

DEFAULT_CONTENT = [
    ("home.hero.eyebrow",       "Guernsey's Professional Network"),
    ("home.hero.title",         "Rooted in Guernsey. Built for everyone."),
    ("home.hero.subtitle",      "Connect Guernsey is a professional network where ambition, experience and fresh perspective come together. We connect people across industries and backgrounds — strengthening the fabric of our island community."),
    ("home.mission.title",      "Growing together, as one community"),
    ("home.mission.body",       "Connect Guernsey was created to bring the island's professional community closer together. We believe the strongest networks are built not just on shared industry, but on shared purpose — a genuine commitment to Guernsey and to one another."),
    ("home.mission.body2",      "Whether you were born here, have made Guernsey your home, or are building your career on this island — Connect Guernsey is your community. We exist to create the connections that help everyone thrive."),
    ("home.community.title",    "Different journeys. One destination."),
    ("home.community.body",     "Our members have taken many different paths to get here — but they share something in common: a commitment to Guernsey, to professional excellence, and to each other. Connect Guernsey is where those paths converge."),
    ("home.cta.title",          "Your place in Guernsey's network."),
    ("home.cta.body",           "Connect Guernsey is launching in 2026. Whether you've lived here your whole life or arrived more recently — this is your community too. Register your interest and be part of it from day one."),
    ("about.hero.title",        "About Connect Guernsey"),
    ("about.story.title",       "Our Founding Story"),
    ("about.story.body",        "Connect Guernsey was founded in November 2025 by a group of professionals who shared a simple belief: that Guernsey deserved a professional network that truly reflected its community — diverse, ambitious, and deeply committed to the island.\n\nWhat started as a conversation quickly became a movement. Within weeks, connections were being made, support was pouring in from Guernsey's Chamber of Commerce, Innovate Guernsey, and other leading organisations. It became clear that this was something the island had long needed.\n\nWe are currently in the process of formally incorporating as a company limited by guarantee, with our official launch planned for May 2026."),
    ("about.mission.title",     "Our Mission"),
    ("about.mission.body",      "To build a professional community that brings Guernsey's people — from every industry and background — closer together, creating the connections that drive careers, grow businesses, and strengthen the island."),
    ("about.vision.title",      "Our Vision"),
    ("about.vision.body",       "A Guernsey where every professional — regardless of where they came from or how long they've been here — has access to a network that supports their growth and helps them contribute to the island's future."),
    ("membership.hero.title",   "Become a Member"),
    ("membership.why.title",    "Why Join Connect Guernsey?"),
    ("membership.why.body",     "Membership of Connect Guernsey gives you access to a growing network of professionals across every major industry on the island. From exclusive events to mentorship opportunities, being a member puts you at the heart of Guernsey's professional community."),
    ("partners.hero.title",     "Partners & Collaborators"),
    ("partners.hero.body",      "Connect Guernsey is proud to work alongside organisations that share our commitment to Guernsey's professional community. We are always open to new partnerships that help us better serve our members and the island."),
    ("contact.hero.title",      "Get in Touch"),
    ("contact.hero.body",       "Whether you're interested in membership, partnership, speaking at an event, or simply want to know more about Connect Guernsey — we'd love to hear from you."),
]

DEFAULT_SETTINGS = [
    ("site_name",       "Connect Guernsey"),
    ("site_tagline",    "Network · Grow · Belong"),
    ("site_email",      "hello@connectguernsey.gg"),
    ("social_linkedin", ""),
    ("social_facebook", ""),
    ("social_instagram",""),
    ("launch_date",     "May 2026"),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    db = get_supabase()

    # Bootstrap first admin
    if not db.table("admins").select("id").execute().data:
        db.table("admins").insert({"name": "Admin", "email": s.ADMIN_EMAIL,
            "password_hash": hash_password(s.ADMIN_PASSWORD), "is_active": True}).execute()
        print(f"✅ First admin created: {s.ADMIN_EMAIL}")

    # Seed content blocks
    existing_keys = {r["key"] for r in db.table("content_blocks").select("key").execute().data}
    for key, value in DEFAULT_CONTENT:
        if key not in existing_keys:
            db.table("content_blocks").insert({"key": key, "value": value}).execute()

    # Seed site settings
    existing_settings = {r["key"] for r in db.table("site_settings").select("key").execute().data}
    for key, value in DEFAULT_SETTINGS:
        if key not in existing_settings:
            db.table("site_settings").insert({"key": key, "value": value}).execute()

    print("✅ Connect Guernsey API ready")
    yield

app = FastAPI(title="Connect Guernsey API", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

for r in [auth_router, members_router, events_router, blog_router, team_router,
          gallery_router, partners_router, enquiries_router, content_router,
          settings_router, admins_router, media_router]:
    app.include_router(r)

@app.get("/")
async def root():
    return {"message": "Connect Guernsey API", "docs": "/docs", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
