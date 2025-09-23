from dotenv import load_dotenv
import os
from supabase import create_client
import jwt

load_dotenv()

auth_header = request.headers.get("Authorization")
token = auth_header.split(" ")[1]

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

response = (
    supabase.table("biomedical_profiles")
    .select("allergies, illnesses, weight, height_cm")
    .eq("user_id", user_id)
    .execute()
)

if response.data:
    print("Success!")
    print(response.data)
else:
    raise Exception(f"Non-success status code: {response.status_code}")