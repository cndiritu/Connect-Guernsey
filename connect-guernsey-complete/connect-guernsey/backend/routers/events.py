from fastapi import APIRouter, HTTPException, Depends
from models.schemas import EventCreate, EventUpdate, RSVPCreate
from core.auth import get_current_admin
from core.database import get_supabase
from core.email import rsvp_confirmation
from slugify import slugify
from typing import Optional

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("/public")
async def public_events():
    db = get_supabase()
    r = db.table("events").select("*").eq("is_published", True).order("event_date").execute()
    return {"events": r.data}

@router.get("/public/{slug}")
async def public_event(slug: str):
    db = get_supabase()
    r = db.table("events").select("*").eq("slug", slug).eq("is_published", True).execute()
    if not r.data: raise HTTPException(404, "Event not found")
    return r.data[0]

@router.post("/rsvp", status_code=201)
async def rsvp(body: RSVPCreate):
    db = get_supabase()
    event = db.table("events").select("*").eq("id", body.event_id).eq("is_published", True).execute()
    if not event.data: raise HTTPException(404, "Event not found")
    if db.table("rsvps").select("id").eq("event_id", body.event_id).eq("email", body.email).execute().data:
        raise HTTPException(400, "Already RSVP'd for this event")
    db.table("rsvps").insert(body.model_dump()).execute()
    e = event.data[0]
    await rsvp_confirmation(body.email, body.first_name, e["title"],
                            e["event_date"][:10] if e.get("event_date") else "TBC")
    return {"message": "RSVP confirmed! We look forward to seeing you."}

@router.get("/")
async def list_events(admin=Depends(get_current_admin)):
    r = get_supabase().table("events").select("*").order("event_date", desc=True).execute()
    return {"events": r.data}

@router.post("/", status_code=201)
async def create_event(body: EventCreate, admin=Depends(get_current_admin)):
    db = get_supabase()
    data = body.model_dump()
    data["slug"] = data.get("slug") or slugify(data["title"])
    for f in ["event_date","end_date"]:
        if data.get(f): data[f] = data[f].isoformat()
    r = db.table("events").insert(data).execute()
    return r.data[0]

@router.patch("/{event_id}")
async def update_event(event_id: str, body: EventUpdate, admin=Depends(get_current_admin)):
    db = get_supabase()
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    for f in ["event_date","end_date"]:
        if f in data: data[f] = data[f].isoformat()
    r = db.table("events").update(data).eq("id", event_id).execute()
    if not r.data: raise HTTPException(404, "Event not found")
    return r.data[0]

@router.post("/{event_id}/publish")
async def publish(event_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("events").update({"is_published": True}).eq("id", event_id).execute()
    return {"message": "Published"}

@router.post("/{event_id}/unpublish")
async def unpublish(event_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("events").update({"is_published": False}).eq("id", event_id).execute()
    return {"message": "Unpublished"}

@router.get("/{event_id}/rsvps")
async def event_rsvps(event_id: str, admin=Depends(get_current_admin)):
    r = get_supabase().table("rsvps").select("*").eq("event_id", event_id).execute()
    return {"rsvps": r.data, "count": len(r.data)}

@router.delete("/{event_id}")
async def delete_event(event_id: str, admin=Depends(get_current_admin)):
    db = get_supabase()
    db.table("rsvps").delete().eq("event_id", event_id).execute()
    db.table("events").delete().eq("id", event_id).execute()
    return {"message": "Event deleted"}
