from fastapi import APIRouter, HTTPException, Depends
from models.schemas import LoginRequest, TokenResponse, AdminCreate
from core.auth import hash_password, verify_password, create_access_token, get_current_admin
from core.database import get_supabase

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login")
async def login(body: LoginRequest):
    db = get_supabase()
    r = db.table("admins").select("*").eq("email", body.email).eq("is_active", True).execute()
    if not r.data or not verify_password(body.password, r.data[0]["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    a = r.data[0]
    token = create_access_token({"sub": a["email"], "role": "admin"})
    return {"access_token": token, "token_type": "bearer",
            "admin": {"id": a["id"], "name": a["name"], "email": a["email"]}}

@router.get("/me")
async def me(admin=Depends(get_current_admin)):
    return {"id": admin["id"], "name": admin["name"], "email": admin["email"]}

@router.post("/change-password")
async def change_password(body: dict, admin=Depends(get_current_admin)):
    if not verify_password(body.get("current_password",""), admin["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    db = get_supabase()
    db.table("admins").update({"password_hash": hash_password(body["new_password"])}).eq("id", admin["id"]).execute()
    return {"message": "Password updated"}
