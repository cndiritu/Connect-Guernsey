# Supabase Database Setup

Copy and paste this entire block into Supabase → SQL Editor → New Query → Run.

```sql
create extension if not exists "uuid-ossp";

create table admins (
  id uuid primary key default uuid_generate_v4(),
  name text not null, email text unique not null,
  password_hash text not null, is_active boolean default true,
  created_at timestamptz default now()
);

create table members (
  id uuid primary key default uuid_generate_v4(),
  first_name text not null, last_name text not null,
  email text unique not null, phone text, industry text,
  company text, bio text, linkedin_url text, image_url text,
  status text default 'pending' check (status in ('pending','approved','suspended')),
  created_at timestamptz default now()
);

create table events (
  id uuid primary key default uuid_generate_v4(),
  title text not null, slug text unique not null,
  description text not null, short_description text,
  event_date timestamptz not null, end_date timestamptz,
  location text not null,
  event_type text default 'open' check (event_type in ('open','members_only')),
  capacity int, image_url text, is_published boolean default false,
  created_at timestamptz default now()
);

create table rsvps (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid references events(id) on delete cascade,
  first_name text not null, last_name text not null,
  email text not null, created_at timestamptz default now(),
  unique(event_id, email)
);

create table team_members (
  id uuid primary key default uuid_generate_v4(),
  name text not null, role text not null,
  board_type text not null check (board_type in ('board','committee','sub_committee')),
  pillar text, bio text, image_url text, linkedin_url text,
  display_order int default 0, is_active boolean default true,
  created_at timestamptz default now()
);

create table content_blocks (
  id uuid primary key default uuid_generate_v4(),
  key text unique not null, value text not null,
  updated_at timestamptz default now()
);

create table enquiries (
  id uuid primary key default uuid_generate_v4(),
  first_name text not null, last_name text not null,
  email text not null, interest text not null,
  industry text, message text not null,
  status text default 'unread' check (status in ('unread','read','replied')),
  created_at timestamptz default now()
);

create table blog_posts (
  id uuid primary key default uuid_generate_v4(),
  title text not null, slug text unique not null,
  excerpt text, content text not null,
  category text, image_url text, author text,
  is_published boolean default false, published_at timestamptz,
  created_at timestamptz default now()
);

create table gallery_albums (
  id uuid primary key default uuid_generate_v4(),
  title text not null, description text,
  event_id uuid references events(id) on delete set null,
  cover_image_url text, is_published boolean default false,
  created_at timestamptz default now()
);

create table gallery_photos (
  id uuid primary key default uuid_generate_v4(),
  album_id uuid references gallery_albums(id) on delete cascade,
  image_url text not null, caption text, display_order int default 0,
  created_at timestamptz default now()
);

create table partners (
  id uuid primary key default uuid_generate_v4(),
  name text not null, description text, logo_url text, website_url text,
  partner_type text default 'partner', display_order int default 0,
  is_active boolean default true, created_at timestamptz default now()
);

create table site_settings (
  id uuid primary key default uuid_generate_v4(),
  key text unique not null, value text not null,
  updated_at timestamptz default now()
);

-- Enable RLS and allow service role full access on all tables
do $$ declare t text; begin
  foreach t in array array['admins','members','events','rsvps','team_members',
    'content_blocks','enquiries','blog_posts','gallery_albums','gallery_photos',
    'partners','site_settings']
  loop
    execute format('alter table %I enable row level security', t);
    execute format('create policy "service_full" on %I for all using (true)', t);
  end loop;
end $$;
```

## Storage Bucket

In Supabase → Storage → New Bucket:
- Name: `connect-guernsey`
- Public: **ON**
