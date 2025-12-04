from supabase import create_client, Client
import httpx
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

http_client = httpx.Client(http2=False)

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    http_client=http_client
)