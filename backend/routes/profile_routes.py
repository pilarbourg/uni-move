from supabase import create_client, Client
from flask import Blueprint, jsonify, request
import jwt

profile_routes = Blueprint("profile_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

JWT_SECRET = "secretkeyforjwt"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@profile_routes.route("/api/profile", methods=["GET", "POST"])
def profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "Missing token"}), 401
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    try:
        email = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])["email"]
    except:
        return jsonify({"message": "Invalid token"}), 401

    if request.method == "GET":
        profile = supabase.table("profile").select("*").eq("email", email).execute()
        if profile.data:
            data = profile.data[0]
            data["registered"] = True
            return jsonify(data), 200
        return jsonify({"name": "", "hobby": "", "nationality": "", "registered": False})

    users = supabase.table("users").select("*").eq("email", email).execute().data[0]
    users_id = users["id"]

    supabase.table("profile").upsert({
        "users_id": users_id,
        "name": data.get("name", ""),
        "hobby": data.get("hobby", ""),
        "nationality": data.get("nationality", "")
    }, on_conflict="users_id").execute()

    return jsonify({"message": "Profile saved", "registered": True}), 200
