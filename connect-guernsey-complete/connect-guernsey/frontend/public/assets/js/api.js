const API_BASE = window.API_BASE || 'https://connect-guernsey.onrender.com';

const api = {
  async get(path) {
    const r = await fetch(`${API_BASE}${path}`);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  },
  async post(path, data) {
    const r = await fetch(`${API_BASE}${path}`, {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
    });
    const json = await r.json();
    if (!r.ok) throw new Error(json.detail || 'Request failed');
    return json;
  }
};

let _content = null, _settings = null;

async function loadContent() {
  if (_content) return _content;
  try { _content = await api.get('/api/content/public'); } catch { _content = {}; }
  return _content;
}

async function loadSettings() {
  if (_settings) return _settings;
  try { _settings = await api.get('/api/settings/public'); } catch { _settings = {}; }
  return _settings;
}

function fillAll() {
  if (!_content) return;
  document.querySelectorAll('[data-content]').forEach(el => {
    const v = _content[el.dataset.content];
    if (v !== undefined) el.textContent = v;
  });
}

function buildNav(activePage = '') {
  const nav = document.getElementById('nav');
  if (!nav) return;
  const links = [
    {href:'/index.html',label:'Home',key:'home'},
    {href:'/about.html',label:'About',key:'about'},
    {href:'/membership.html',label:'Membership',key:'membership'},
    {href:'/events.html',label:'Events',key:'events'},
    {href:'/blog.html',label:'Blog',key:'blog'},
    {href:'/gallery.html',label:'Gallery',key:'gallery'},
    {href:'/partners.html',label:'Partners',key:'partners'},
    {href:'/contact.html',label:'Contact',key:'contact'},
  ];
  nav.innerHTML = `
    <a href="/index.html" class="nav-logo">
      <div class="nav-diamond"><span>CG</span></div>
      Connect Guernsey
    </a>
    <div class="nav-links">
      ${links.map(l=>`<a href="${l.href}" class="${l.key===activePage?'active':''}">${l.label}</a>`).join('')}
      <a href="/membership.html#register" class="nav-join">Join Us</a>
    </div>
    <button class="nav-burger" onclick="toggleMobileNav()">☰</button>`;
  const mn = document.getElementById('mobile-nav');
  if (mn) mn.innerHTML = links.map(l=>`<a href="${l.href}">${l.label}</a>`).join('') +
    `<a href="/membership.html#register" class="btn btn-gold" style="text-align:center">Join Us</a>`;
}

function toggleMobileNav() {
  document.getElementById('mobile-nav')?.classList.toggle('open');
}

function buildFooter() {
  const f = document.querySelector('footer');
  if (!f) return;
  f.innerHTML = `
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/index.html" class="nav-logo" style="margin-bottom:1rem"><div class="nav-diamond"><span>CG</span></div>Connect Guernsey</a>
        <p>Guernsey's professional network — connecting ambitious people across industries and backgrounds, and weaving those connections into the life of our island.</p>
        <div class="footer-mosaic" style="margin-top:1.5rem">
          ${['terra','amber','forest','cobalt','violet','gold','teal','rose'].map(c=>`<span style="background:var(--${c})"></span>`).join('')}
        </div>
      </div>
      <div class="footer-col"><h4>Organisation</h4><a href="/index.html">Home</a><a href="/about.html">About Us</a><a href="/about.html#founding-story">Founding Story</a><a href="/about.html#leadership">Leadership</a><a href="/about.html#pillars">Our Pillars</a></div>
      <div class="footer-col"><h4>Get Involved</h4><a href="/membership.html">Membership</a><a href="/events.html">Events</a><a href="/gallery.html">Gallery</a><a href="/blog.html">Blog & News</a></div>
      <div class="footer-col"><h4>Connect</h4><a href="/contact.html">Contact Us</a><a href="/partners.html">Partnerships</a><a href="/partners.html#sponsor">Sponsorship</a><a href="#" id="f-linkedin">LinkedIn</a><a href="#" id="f-facebook">Facebook</a></div>
    </div>
    <div class="footer-bottom"><p>© 2026 Connect Guernsey. All rights reserved.</p><p><a href="/legal.html" style="color:inherit">Privacy Policy</a> · <a href="/legal.html#terms" style="color:inherit">Terms</a></p></div>`;
  loadSettings().then(s => {
    const li = document.getElementById('f-linkedin');
    const fb = document.getElementById('f-facebook');
    if (li && s.social_linkedin) li.href = s.social_linkedin;
    if (fb && s.social_facebook) fb.href = s.social_facebook;
  });
}

function initReveal() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, {threshold: 0.08});
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

function formatDate(s) {
  if (!s) return 'TBC';
  return new Date(s).toLocaleDateString('en-GB', {day:'numeric',month:'long',year:'numeric'});
}
function formatMonth(s) {
  if (!s) return '';
  return new Date(s).toLocaleDateString('en-GB', {month:'short',year:'numeric'});
}
function showAlert(id, msg, type='success') {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => { if(el) el.innerHTML=''; }, 6000);
}

document.addEventListener('DOMContentLoaded', () => { buildFooter(); initReveal(); });
