import os
from supabase import create_client, Client

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    return create_client(url, key)

# Also expose as supabase for any code that imports it directly
def get_supabase() -> Client:
    return get_client()
