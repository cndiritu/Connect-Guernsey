from fastapi import APIRouter, HTTPException, Depends
from models.schemas import BlogPostCreate, BlogPostUpdate
from core.auth import get_current_admin
from core.database import get_supabase
from slugify import slugify
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/blog", tags=["Blog"])

@router.get("/public")
async def public_posts(category: Optional[str]=None, limit: int=12, offset: int=0):
    db = get_supabase()
    q = db.table("blog_posts").select("id,title,slug,excerpt,category,image_url,published_at,author")\
          .eq("is_published", True).order("published_at", desc=True).range(offset, offset+limit-1)
    if category: q = q.eq("category", category)
    return {"posts": q.execute().data}

@router.get("/public/{slug}")
async def public_post(slug: str):
    db = get_supabase()
    r = db.table("blog_posts").select("*").eq("slug", slug).eq("is_published", True).execute()
    if not r.data: raise HTTPException(404, "Post not found")
    return r.data[0]

@router.get("/")
async def list_posts(admin=Depends(get_current_admin)):
    r = get_supabase().table("blog_posts").select("*").order("created_at", desc=True).execute()
    return {"posts": r.data}

@router.post("/", status_code=201)
async def create_post(body: BlogPostCreate, admin=Depends(get_current_admin)):
    db = get_supabase()
    data = body.model_dump()
    data["slug"] = data.get("slug") or slugify(data["title"])
    data["author"] = admin["name"]
    if data.get("published_at"): data["published_at"] = data["published_at"].isoformat()
    if data["is_published"] and not data.get("published_at"):
        data["published_at"] = datetime.utcnow().isoformat()
    r = db.table("blog_posts").insert(data).execute()
    return r.data[0]

@router.patch("/{post_id}")
async def update_post(post_id: str, body: BlogPostUpdate, admin=Depends(get_current_admin)):
    db = get_supabase()
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    if data.get("published_at"): data["published_at"] = data["published_at"].isoformat()
    if data.get("is_published") and not data.get("published_at"):
        data["published_at"] = datetime.utcnow().isoformat()
    r = db.table("blog_posts").update(data).eq("id", post_id).execute()
    if not r.data: raise HTTPException(404, "Post not found")
    return r.data[0]

@router.delete("/{post_id}")
async def delete_post(post_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("blog_posts").delete().eq("id", post_id).execute()
    return {"message": "Post deleted"}
