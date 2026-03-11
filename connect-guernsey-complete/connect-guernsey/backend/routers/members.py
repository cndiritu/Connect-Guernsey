from fastapi import APIRouter, HTTPException, Depends
from models.schemas import MemberCreate, MemberUpdate
from core.auth import get_current_admin
from core.database import get_supabase
from core.email import welcome_email
from typing import Optional

router = APIRouter(prefix="/api/members", tags=["Members"])

@router.post("/register", status_code=201)
async def register(body: MemberCreate):
    db = get_supabase()
    if db.table("members").select("id").eq("email", body.email).execute().data:
        raise HTTPException(400, "Email already registered")
    data = body.model_dump()
    data["status"] = "pending"
    r = db.table("members").insert(data).execute()
    await welcome_email(r.data[0]["email"], r.data[0]["first_name"])
    return {"message": "Registration received. We'll be in touch soon.", "id": r.data[0]["id"]}

@router.get("/")
async def list_members(status: Optional[str]=None, search: Optional[str]=None,
                       limit: int=50, offset: int=0, admin=Depends(get_current_admin)):
    db = get_supabase()
    q = db.table("members").select("*").order("created_at", desc=True).range(offset, offset+limit-1)
    if status: q = q.eq("status", status)
    if search: q = q.or_(f"first_name.ilike.%{search}%,last_name.ilike.%{search}%,email.ilike.%{search}%")
    r = q.execute()
    return {"members": r.data, "count": len(r.data)}

@router.get("/stats")
async def stats(admin=Depends(get_current_admin)):
    db = get_supabase()
    all_m = db.table("members").select("status").execute().data
    return {"total": len(all_m),
            "pending": sum(1 for m in all_m if m["status"]=="pending"),
            "approved": sum(1 for m in all_m if m["status"]=="approved"),
            "suspended": sum(1 for m in all_m if m["status"]=="suspended")}

@router.get("/{member_id}")
async def get_member(member_id: str, admin=Depends(get_current_admin)):
    db = get_supabase()
    r = db.table("members").select("*").eq("id", member_id).execute()
    if not r.data: raise HTTPException(404, "Member not found")
    return r.data[0]

@router.patch("/{member_id}")
async def update_member(member_id: str, body: MemberUpdate, admin=Depends(get_current_admin)):
    db = get_supabase()
    data = {k:v for k,v in body.model_dump().items() if v is not None}
    r = db.table("members").update(data).eq("id", member_id).execute()
    if not r.data: raise HTTPException(404, "Member not found")
    return r.data[0]

@router.post("/{member_id}/approve")
async def approve(member_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("members").update({"status":"approved"}).eq("id", member_id).execute()
    return {"message": "Member approved"}

@router.post("/{member_id}/suspend")
async def suspend(member_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("members").update({"status":"suspended"}).eq("id", member_id).execute()
    return {"message": "Member suspended"}

@router.delete("/{member_id}")
async def delete_member(member_id: str, admin=Depends(get_current_admin)):
    get_supabase().table("members").delete().eq("id", member_id).execute()
    return {"message": "Member deleted"}
