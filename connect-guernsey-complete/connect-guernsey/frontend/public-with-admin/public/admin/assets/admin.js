const API_BASE = 'https://connect-guernsey.onrender.com';

const adminApi = {
  async req(method, path, data, isForm=false) {
    const headers = {};
    const token = localStorage.getItem('cg_token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (!isForm) headers['Content-Type'] = 'application/json';
    const opts = { method, headers };
    if (data) opts.body = isForm ? data : JSON.stringify(data);
    const r = await fetch(`${API_BASE}${path}`, opts);
    if (r.status === 401) { logout(); return; }
    const json = await r.json().catch(()=>({}));
    if (!r.ok) throw new Error(json.detail || `Error ${r.status}`);
    return json;
  },
  get: (p) => adminApi.req('GET', p),
  post: (p, d) => adminApi.req('POST', p, d),
  patch: (p, d) => adminApi.req('PATCH', p, d),
  put: (p, d) => adminApi.req('PUT', p, d),
  delete: (p) => adminApi.req('DELETE', p),
  upload: (p, fd) => adminApi.req('POST', p, fd, true),
};

let _admin = JSON.parse(localStorage.getItem('cg_admin')||'null');

function requireAuth() {
  if (!localStorage.getItem('cg_token')) { location.href = '/admin/index.html'; return false; }
  return true;
}

function logout() {
  localStorage.removeItem('cg_token');
  localStorage.removeItem('cg_admin');
  location.href = '/admin/index.html';
}

function buildSidebar(activePage) {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;
  const initials = _admin ? _admin.name.split(' ').map(n=>n[0]).join('').toUpperCase().slice(0,2) : 'AD';
  sidebar.innerHTML = `
    <div class="sidebar-logo">
      <div class="sidebar-logo-diamond"><span>CG</span></div>
      <div><div class="sidebar-logo-text">Connect Guernsey</div><div class="sidebar-logo-sub">Admin Panel</div></div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section-title">Overview</div>
      <a href="/admin/dashboard.html" class="nav-item ${activePage==='dashboard'?'active':''}"><span class="icon">📊</span> Dashboard</a>
      <div class="nav-section-title">Content</div>
      <a href="/admin/events.html" class="nav-item ${activePage==='events'?'active':''}"><span class="icon">🗓</span> Events</a>
      <a href="/admin/blog.html" class="nav-item ${activePage==='blog'?'active':''}"><span class="icon">✍️</span> Blog</a>
      <a href="/admin/gallery.html" class="nav-item ${activePage==='gallery'?'active':''}"><span class="icon">📷</span> Gallery</a>
      <a href="/admin/pages.html" class="nav-item ${activePage==='pages'?'active':''}"><span class="icon">📄</span> Page Content</a>
      <div class="nav-section-title">Community</div>
      <a href="/admin/members.html" class="nav-item ${activePage==='members'?'active':''}"><span class="icon">👥</span> Members</a>
      <a href="/admin/team.html" class="nav-item ${activePage==='team'?'active':''}"><span class="icon">⭐</span> Team</a>
      <a href="/admin/enquiries.html" class="nav-item ${activePage==='enquiries'?'active':''}"><span class="icon">✉️</span> Enquiries</a>
      <div class="nav-section-title">Setup</div>
      <a href="/admin/partners.html" class="nav-item ${activePage==='partners'?'active':''}"><span class="icon">🤝</span> Partners</a>
      <a href="/admin/settings.html" class="nav-item ${activePage==='settings'?'active':''}"><span class="icon">⚙️</span> Settings</a>
      <a href="/" target="_blank" class="nav-item"><span class="icon">🌐</span> View Site</a>
    </nav>
    <div class="sidebar-footer">
      <div class="sidebar-user">
        <div class="su-avatar">${initials}</div>
        <div><div class="su-name">${_admin?.name||'Admin'}</div><div class="su-role">Administrator</div></div>
      </div>
      <button class="btn-logout" onclick="logout()">Sign Out</button>
    </div>`;
}

function showAlert(id, msg, type='success') {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => { if(el) el.innerHTML=''; }, 5000);
}

function formatDate(s) {
  if (!s) return '—';
  return new Date(s).toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'});
}
function formatDateTime(s) {
  if (!s) return '—';
  return new Date(s).toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
}

function initEditor(containerId, textareaId) {
  const container = document.getElementById(containerId);
  const textarea = document.getElementById(textareaId);
  if (!container || !textarea) return;
  container.innerHTML = `
    <div class="rich-editor">
      <div class="editor-toolbar">
        <button class="et-btn" onclick="execCmd('bold')"><strong>B</strong></button>
        <button class="et-btn" onclick="execCmd('italic')"><em>I</em></button>
        <button class="et-btn" onclick="execCmd('underline')"><u>U</u></button>
        <button class="et-btn" onclick="execCmd('insertUnorderedList')">• List</button>
        <button class="et-btn" onclick="execCmd('formatBlock','h2')">H2</button>
        <button class="et-btn" onclick="execCmd('formatBlock','p')">P</button>
      </div>
      <div class="editor-area" id="${containerId}_area" contenteditable="true"></div>
    </div>`;
  const area = document.getElementById(`${containerId}_area`);
  area.innerHTML = textarea.value;
  area.addEventListener('input', () => { textarea.value = area.innerHTML; });
}
function execCmd(cmd, val) { document.execCommand(cmd, false, val||null); }
