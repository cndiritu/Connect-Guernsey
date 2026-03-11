from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: dict

class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    industry: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    status: Optional[str] = None

class EventCreate(BaseModel):
    title: str
    slug: Optional[str] = None
    description: str
    short_description: Optional[str] = None
    event_date: datetime
    end_date: Optional[datetime] = None
    location: str
    event_type: str = "open"
    capacity: Optional[int] = None
    image_url: Optional[str] = None
    is_published: bool = False

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    event_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    event_type: Optional[str] = None
    capacity: Optional[int] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None

class RSVPCreate(BaseModel):
    event_id: str
    first_name: str
    last_name: str
    email: EmailStr

class TeamMemberCreate(BaseModel):
    name: str
    role: str
    board_type: str
    pillar: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    display_order: int = 0

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    board_type: Optional[str] = None
    pillar: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class ContentUpdate(BaseModel):
    value: str

class EnquiryCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    interest: str
    industry: Optional[str] = None
    message: str

class BlogPostCreate(BaseModel):
    title: str
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: str
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool = False
    published_at: Optional[datetime] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None

class GalleryAlbumCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_id: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: bool = False

class GalleryPhotoCreate(BaseModel):
    album_id: str
    image_url: str
    caption: Optional[str] = None
    display_order: int = 0

class PartnerCreate(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    partner_type: str = "partner"
    display_order: int = 0
    is_active: bool = True

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    partner_type: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class SiteSettingUpdate(BaseModel):
    value: str
