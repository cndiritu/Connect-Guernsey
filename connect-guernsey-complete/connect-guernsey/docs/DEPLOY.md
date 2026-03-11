# Deployment Guide — Connect Guernsey

Plain English, step by step. No tech experience needed beyond copy-paste.

---

## What You Need (All Free)

| Service | What it does | Cost |
|---------|-------------|------|
| **Supabase** | Database + file storage | Free |
| **Render** | Runs the backend API | Free |
| **Netlify** | Hosts the website | Free |
| **Resend** | Sends emails | Free (100/day) |

---

## Step 1 — Set Up Supabase (Database)

1. Go to **supabase.com** → Sign up → New Project
2. Choose a name (e.g. `connect-guernsey`) and a strong password → Create
3. Wait ~2 minutes for it to set up
4. Go to **SQL Editor** → New Query
5. Copy everything from `docs/SUPABASE.md` (the SQL block) and paste it → Run
6. Go to **Storage** → New Bucket → Name: `connect-guernsey` → Public: ON → Create
7. Go to **Project Settings** → API:
   - Copy the **Project URL** — save this as `SUPABASE_URL`
   - Copy the **service_role** key (secret) — save this as `SUPABASE_SERVICE_KEY`

---

## Step 2 — Set Up Resend (Email)

1. Go to **resend.com** → Sign up → Create API Key
2. Copy the key — save it as `RESEND_API_KEY`
3. Add your domain (e.g. `connectguernsey.gg`) in Resend → Domains → follow DNS instructions
4. Your `EMAIL_FROM` will be e.g. `hello@connectguernsey.gg`

*(If you don't have a domain yet, skip email for now — everything works without it, just no email confirmations.)*

---

## Step 3 — Deploy Backend to Render

1. Push the project to **GitHub** (create a free account, then a new repository, upload the whole folder)
2. Go to **render.com** → Sign up → New → Web Service
3. Connect your GitHub repo
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
5. Add Environment Variables (click "Add Environment Variable" for each):

```
SUPABASE_URL         = (paste your Supabase URL)
SUPABASE_SERVICE_KEY = (paste your service_role key)
JWT_SECRET           = (make up a long random string, e.g. connectguernsey2026secretkey!)
ADMIN_EMAIL          = admin@connectguernsey.gg
ADMIN_PASSWORD       = (choose a strong password)
RESEND_API_KEY       = (paste your Resend key)
EMAIL_FROM           = hello@connectguernsey.gg
FRONTEND_URL         = https://connectguernsey.gg
ENVIRONMENT          = production
```

6. Click **Deploy** — wait ~3 minutes
7. Copy your backend URL — it looks like: `https://connect-guernsey-api.onrender.com`

---

## Step 4 — Update Frontend API URL

Before deploying the frontend, tell it where your backend is:

1. Open `frontend/public/assets/js/api.js`
2. Find the first line: `const API_BASE = window.API_BASE || 'http://localhost:8000';`
3. Change it to: `const API_BASE = window.API_BASE || 'https://your-backend.onrender.com';`
4. Do the same in `frontend/admin/assets/admin.js` — same line, same change
5. Save both files

---

## Step 5 — Deploy Frontend to Netlify

1. Go to **netlify.com** → Sign up → Add New Site → Deploy Manually
2. Drag and drop the entire `frontend` folder into the Netlify deploy box
3. Wait ~30 seconds — you'll get a URL like `https://amazing-site-123.netlify.app`
4. (Optional) Go to Site Settings → Domain Management → Add your custom domain

---

## Step 6 — First Login

1. Go to `https://your-site.netlify.app/admin/index.html`
2. Log in with:
   - Email: the `ADMIN_EMAIL` you set in Render
   - Password: the `ADMIN_PASSWORD` you set in Render
3. **Change your password immediately** in Settings → Admin Account

---

## Step 7 — Add Your Team

1. In the admin → Team Members → Add the board, committee, and sub-committee members
2. They'll automatically appear on the About page

---

## Step 8 — Add Your First Event

1. Admin → Events → New Event
2. Fill in the official launch details
3. Toggle "Publish immediately" → Save
4. It appears live on the website instantly

---

## Ongoing Usage

| Task | Where |
|------|-------|
| Approve new members | Admin → Members → Pending |
| Write a blog post | Admin → Blog → New Post |
| Add event photos | Admin → Gallery → New Album |
| Edit website text | Admin → Page Content |
| Check enquiries | Admin → Enquiries |
| Update social links | Admin → Settings |

---

## Troubleshooting

**Backend won't start:** Check all environment variables are set correctly in Render.

**"CORS error" in browser:** Make sure `FRONTEND_URL` in Render matches your actual Netlify URL exactly (no trailing slash).

**Emails not sending:** Check your `RESEND_API_KEY` is correct and your domain is verified in Resend.

**Can't log in to admin:** Make sure the backend deployed successfully — check Render logs.

**Free tier note:** Render free tier spins down after 15 mins of inactivity. First request after idle takes ~30 seconds. Upgrade to Render Starter ($7/mo) to avoid this.

---

## Your URLs

Once deployed, bookmark these:

- **Website:** `https://your-site.netlify.app`
- **Admin:** `https://your-site.netlify.app/admin/index.html`
- **API docs:** `https://your-backend.onrender.com/docs`
