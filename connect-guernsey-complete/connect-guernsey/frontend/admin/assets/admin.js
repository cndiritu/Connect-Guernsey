const API_BASE = 'https://connect-guernsey.onrender.com';

const api = {
  async post(path, data, token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(API_BASE + path, { method: 'POST', headers, body: JSON.stringify(data) });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Request failed');
    return json;
  },
  async get(path, token) {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(API_BASE + path, { headers });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Request failed');
    return json;
  },
  async put(path, data, token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(API_BASE + path, { method: 'PUT', headers, body: JSON.stringify(data) });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Request failed');
    return json;
  },
  async delete(path, token) {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(API_BASE + path, { method: 'DELETE', headers });
    if (!res.ok) { const json = await res.json(); throw new Error(json.detail || 'Request failed'); }
    return true;
  }
};

function getToken() { return localStorage.getItem('cg_admin_token'); }
function setToken(t) { localStorage.setItem('cg_admin_token', t); }
function clearToken() { localStorage.removeItem('cg_admin_token'); }

function requireAuth() {
  const token = getToken();
  if (!token) { window.location.href = '/admin/index.html'; return null; }
  return token;
}

function logout() {
  clearToken();
  window.location.href = '/admin/index.html';
}

function showAlert(id, msg, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => el.innerHTML = '', 4000);
}

// Login handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('loginBtn');
    const err = document.getElementById('loginError');
    btn.textContent = 'Signing in...';
    btn.disabled = true;
    err.textContent = '';
    try {
      const data = await api.post('/api/auth/login', {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
      });
      setToken(data.access_token);
      window.location.href = '/admin/dashboard.html';
    } catch(e) {
      err.textContent = e.message || 'Login failed. Please check your credentials.';
      btn.textContent = 'Sign In';
      btn.disabled = false;
    }
  });
}
