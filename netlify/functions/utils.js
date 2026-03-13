const { createClient } = require("@supabase/supabase-js");

let client;

function getSupabase() {
  if (!client) {
    const url = process.env.SUPABASE_URL;
    const key = process.env.SUPABASE_SERVICE_KEY;
    if (!url || !key) {
      throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY");
    }
    client = createClient(url, key);
  }
  return client;
}

const headers = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Content-Type": "application/json",
};

function ok(body) {
  return { statusCode: 200, headers, body: JSON.stringify(body) };
}

function err(status, message) {
  return { statusCode: status, headers, body: JSON.stringify({ detail: message }) };
}

module.exports = { getSupabase, headers, ok, err };
