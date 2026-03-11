import httpx
from core.config import get_settings

BRAND = """<div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;background:#0d1f3c;color:white;padding:40px;">
  <div style="text-align:center;border-bottom:1px solid #c9a84c;padding-bottom:20px;margin-bottom:28px;">
    <h1 style="color:#c9a84c;margin:0;font-size:24px;">Connect Guernsey</h1>
    <p style="color:rgba(255,255,255,0.4);font-size:11px;letter-spacing:.2em;margin:6px 0 0">NETWORK · GROW · BELONG</p>
  </div>
  {body}
  <div style="margin-top:36px;padding-top:20px;border-top:1px solid rgba(201,168,76,.3);text-align:center;">
    <p style="color:rgba(255,255,255,.25);font-size:11px;margin:0;">© 2026 Connect Guernsey · Guernsey, Channel Islands</p>
  </div>
</div>"""

async def send_email(to: str, subject: str, body_html: str):
    s = get_settings()
    if not s.RESEND_API_KEY:
        print(f"[EMAIL - no key configured] To:{to} | {subject}")
        return
    html = BRAND.format(body=body_html)
    async with httpx.AsyncClient() as client:
        await client.post("https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {s.RESEND_API_KEY}"},
            json={"from": s.EMAIL_FROM, "to": to, "subject": subject, "html": html})

async def welcome_email(to: str, name: str):
    await send_email(to, "Welcome to Connect Guernsey",
        f"<h2 style='color:white'>Welcome, {name}!</h2>"
        "<p style='color:rgba(255,255,255,.7);line-height:1.7'>Thank you for registering with Connect Guernsey. "
        "Your application is under review and you'll hear from us shortly.</p>"
        "<p style='color:rgba(255,255,255,.7);line-height:1.7'>We look forward to welcoming you to the community.</p>")

async def enquiry_notification(admin_email: str, name: str, interest: str, message: str):
    await send_email(admin_email, f"New Enquiry: {interest}",
        f"<h2 style='color:#c9a84c'>New Enquiry</h2>"
        f"<p><strong style='color:white'>From:</strong> <span style='color:rgba(255,255,255,.7)'>{name}</span></p>"
        f"<p><strong style='color:white'>Interest:</strong> <span style='color:rgba(255,255,255,.7)'>{interest}</span></p>"
        f"<hr style='border-color:rgba(201,168,76,.3);margin:16px 0'/>"
        f"<p style='color:rgba(255,255,255,.7);line-height:1.7'>{message}</p>")

async def rsvp_confirmation(to: str, name: str, event_title: str, event_date: str):
    await send_email(to, f"RSVP Confirmed: {event_title}",
        f"<h2 style='color:white'>You're confirmed, {name}!</h2>"
        f"<p style='color:rgba(255,255,255,.7);line-height:1.7'>Your RSVP for <strong>{event_title}</strong> on {event_date} is confirmed. We look forward to seeing you there.</p>")
