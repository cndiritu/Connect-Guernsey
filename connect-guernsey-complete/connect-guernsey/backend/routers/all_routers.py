from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from models.schemas import (TeamMemberCreate, TeamMemberUpdate, GalleryAlbumCreate,
    GalleryPhotoCreate, PartnerCreate, PartnerUpdate, EnquiryCreate,
    ContentUpdate, SiteSettingUpdate, AdminCreate, AdminUpdate)
from core.auth import get_current_admin, hash_password
from core.database import get_supabase
from core.email import enquiry_notification
from core.config import get_settings
import uuid, os

# ── TEAM ────────────────────────────────────────────
team_router = APIRouter(prefix="/api/team", tags=["Team"])

@team_router.get("/public")
async def public_team():
    r = get_supabase().table("team_members").select("*").eq("is_active",True).order("display_order").execute()
    return {"team": r.data}

@team_router.get("/")
async def list_team(admin=Depends(get_current_admin)):
    r = get_supabase().table("team_members").select("*").order("display_order").execute()
    return {"team": r.data}

@team_router.post("/", status_code=201)
async def create_member(body: TeamMemberCreate, admin=Depends(get_current_admin)):
    data = body.model_dump(); data["is_active"] = True
    r = get_supabase().table("team_members").insert(data).execute()
    return r.data[0]

@team_router.patch("/{mid}")
async def update_member(mid: str, body: TeamMemberUpdate, admin=Depends(get_current_admin)):
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    r = get_supabase().table("team_members").update(data).eq("id", mid).execute()
    if not r.data: raise HTTPException(404, "Not found")
    return r.data[0]

@team_router.delete("/{mid}")
async def delete_member(mid: str, admin=Depends(get_current_admin)):
    get_supabase().table("team_members").delete().eq("id", mid).execute()
    return {"message": "Removed"}

# ── GALLERY ─────────────────────────────────────────
gallery_router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

@gallery_router.get("/public")
async def public_albums():
    db = get_supabase()
    albums = db.table("gallery_albums").select("*").eq("is_published",True).order("created_at",desc=True).execute().data
    for a in albums:
        photos = db.table("gallery_photos").select("*").eq("album_id", a["id"]).order("display_order").execute().data
        a["photos"] = photos
    return {"albums": albums}

@gallery_router.get("/")
async def list_albums(admin=Depends(get_current_admin)):
    db = get_supabase()
    albums = db.table("gallery_albums").select("*").order("created_at",desc=True).execute().data
    for a in albums:
        count = db.table("gallery_photos").select("id").eq("album_id", a["id"]).execute().data
        a["photo_count"] = len(count)
    return {"albums": albums}

@gallery_router.post("/albums", status_code=201)
async def create_album(body: GalleryAlbumCreate, admin=Depends(get_current_admin)):
    r = get_supabase().table("gallery_albums").insert(body.model_dump()).execute()
    return r.data[0]

@gallery_router.patch("/albums/{aid}")
async def update_album(aid: str, body: dict, admin=Depends(get_current_admin)):
    r = get_supabase().table("gallery_albums").update(body).eq("id", aid).execute()
    return r.data[0] if r.data else {}

@gallery_router.delete("/albums/{aid}")
async def delete_album(aid: str, admin=Depends(get_current_admin)):
    db = get_supabase()
    db.table("gallery_photos").delete().eq("album_id", aid).execute()
    db.table("gallery_albums").delete().eq("id", aid).execute()
    return {"message": "Album deleted"}

@gallery_router.post("/photos", status_code=201)
async def add_photo(body: GalleryPhotoCreate, admin=Depends(get_current_admin)):
    r = get_supabase().table("gallery_photos").insert(body.model_dump()).execute()
    return r.data[0]

@gallery_router.delete("/photos/{pid}")
async def delete_photo(pid: str, admin=Depends(get_current_admin)):
    get_supabase().table("gallery_photos").delete().eq("id", pid).execute()
    return {"message": "Photo deleted"}

# ── PARTNERS ────────────────────────────────────────
partners_router = APIRouter(prefix="/api/partners", tags=["Partners"])

@partners_router.get("/public")
async def public_partners():
    r = get_supabase().table("partners").select("*").eq("is_active",True).order("display_order").execute()
    return {"partners": r.data}

@partners_router.get("/")
async def list_partners(admin=Depends(get_current_admin)):
    r = get_supabase().table("partners").select("*").order("display_order").execute()
    return {"partners": r.data}

@partners_router.post("/", status_code=201)
async def create_partner(body: PartnerCreate, admin=Depends(get_current_admin)):
    r = get_supabase().table("partners").insert(body.model_dump()).execute()
    return r.data[0]

@partners_router.patch("/{pid}")
async def update_partner(pid: str, body: PartnerUpdate, admin=Depends(get_current_admin)):
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    r = get_supabase().table("partners").update(data).eq("id", pid).execute()
    return r.data[0] if r.data else {}

@partners_router.delete("/{pid}")
async def delete_partner(pid: str, admin=Depends(get_current_admin)):
    get_supabase().table("partners").delete().eq("id", pid).execute()
    return {"message": "Partner removed"}

# ── ENQUIRIES ───────────────────────────────────────
enquiries_router = APIRouter(prefix="/api/enquiries", tags=["Enquiries"])

@enquiries_router.post("/", status_code=201)
async def submit(body: EnquiryCreate):
    db = get_supabase(); s = get_settings()
    data = body.model_dump(); data["status"] = "unread"
    db.table("enquiries").insert(data).execute()
    await enquiry_notification(s.ADMIN_EMAIL, f"{body.first_name} {body.last_name}", body.interest, body.message)
    return {"message": "Thank you! We'll be in touch soon."}

@enquiries_router.get("/")
async def list_enquiries(status=None, limit: int=50, offset: int=0, admin=Depends(get_current_admin)):
    db = get_supabase()
    q = db.table("enquiries").select("*").order("created_at",desc=True).range(offset, offset+limit-1)
    if status: q = q.eq("status", status)
    r = q.execute()
    unread = db.table("enquiries").select("id").eq("status","unread").execute()
    return {"enquiries": r.data, "count": len(r.data), "unread": len(unread.data)}

@enquiries_router.patch("/{eid}")
async def update_enquiry(eid: str, body: dict, admin=Depends(get_current_admin)):
    get_supabase().table("enquiries").update(body).eq("id", eid).execute()
    return {"message": "Updated"}

@enquiries_router.delete("/{eid}")
async def delete_enquiry(eid: str, admin=Depends(get_current_admin)):
    get_supabase().table("enquiries").delete().eq("id", eid).execute()
    return {"message": "Deleted"}

# ── CONTENT (CMS) ───────────────────────────────────
content_router = APIRouter(prefix="/api/content", tags=["Content"])

@content_router.get("/public")
async def get_public_content():
    r = get_supabase().table("content_blocks").select("key,value").execute()
    return {row["key"]: row["value"] for row in r.data}

@content_router.get("/")
async def get_content(admin=Depends(get_current_admin)):
    r = get_supabase().table("content_blocks").select("*").order("key").execute()
    sections = {}
    for row in r.data:
        sec = row["key"].split(".")[0]
        sections.setdefault(sec, []).append(row)
    return {"blocks": r.data, "sections": sections}

@content_router.put("/{key}")
async def update_content(key: str, body: ContentUpdate, admin=Depends(get_current_admin)):
    get_supabase().table("content_blocks").upsert({"key": key, "value": body.value}).execute()
    return {"key": key, "value": body.value}

# ── SITE SETTINGS ───────────────────────────────────
settings_router = APIRouter(prefix="/api/settings", tags=["Settings"])

@settings_router.get("/public")
async def get_public_settings():
    r = get_supabase().table("site_settings").select("key,value").execute()
    return {row["key"]: row["value"] for row in r.data}

@settings_router.get("/")
async def get_settings_all(admin=Depends(get_current_admin)):
    r = get_supabase().table("site_settings").select("*").order("key").execute()
    return {"settings": r.data}

@settings_router.put("/{key}")
async def update_setting(key: str, body: SiteSettingUpdate, admin=Depends(get_current_admin)):
    get_supabase().table("site_settings").upsert({"key": key, "value": body.value}).execute()
    return {"key": key, "value": body.value}

# ── ADMINS ──────────────────────────────────────────
admins_router = APIRouter(prefix="/api/admins", tags=["Admins"])

@admins_router.get("/")
async def list_admins(admin=Depends(get_current_admin)):
    r = get_supabase().table("admins").select("id,name,email,is_active,created_at").execute()
    return {"admins": r.data}

@admins_router.post("/", status_code=201)
async def create_admin(body: AdminCreate, admin=Depends(get_current_admin)):
    db = get_supabase()
    if db.table("admins").select("id").eq("email", body.email).execute().data:
        raise HTTPException(400, "Email already exists")
    r = db.table("admins").insert({"name": body.name, "email": body.email,
        "password_hash": hash_password(body.password), "is_active": True}).execute()
    a = r.data[0]
    return {"id": a["id"], "name": a["name"], "email": a["email"]}

@admins_router.patch("/{aid}")
async def update_admin(aid: str, body: AdminUpdate, admin=Depends(get_current_admin)):
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    get_supabase().table("admins").update(data).eq("id", aid).execute()
    return {"message": "Updated"}

@admins_router.delete("/{aid}")
async def delete_admin(aid: str, admin=Depends(get_current_admin)):
    if admin["id"] == aid: raise HTTPException(400, "Cannot delete your own account")
    get_supabase().table("admins").delete().eq("id", aid).execute()
    return {"message": "Admin removed"}

# ── MEDIA ───────────────────────────────────────────
media_router = APIRouter(prefix="/api/media", tags=["Media"])

ALLOWED = {"image/jpeg","image/png","image/webp","image/gif"}

@media_router.post("/upload")
async def upload(file: UploadFile = File(...), admin=Depends(get_current_admin)):
    if file.content_type not in ALLOWED:
        raise HTTPException(400, "Only image files allowed (JPG, PNG, WebP, GIF)")
    contents = await file.read()
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(400, "File must be under 8MB")
    ext = os.path.splitext(file.filename or "img.jpg")[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    path = f"uploads/{filename}"
    db = get_supabase()
    db.storage.from_("connect-guernsey").upload(path, contents, {"content-type": file.content_type})
    url = db.storage.from_("connect-guernsey").get_public_url(path)
    return {"url": url, "filename": filename, "path": path}

@media_router.get("/library")
async def library(admin=Depends(get_current_admin)):
    db = get_supabase()
    try:
        files = db.storage.from_("connect-guernsey").list("uploads")
        result = []
        for f in (files or []):
            url = db.storage.from_("connect-guernsey").get_public_url(f"uploads/{f['name']}")
            result.append({"name": f["name"], "url": url, "size": f.get("metadata",{}).get("size",0)})
        return {"files": result}
    except:
        return {"files": []}

@media_router.delete("/{filename}")
async def delete_file(filename: str, admin=Depends(get_current_admin)):
    get_supabase().storage.from_("connect-guernsey").remove([f"uploads/{filename}"])
    return {"message": "Deleted"}
