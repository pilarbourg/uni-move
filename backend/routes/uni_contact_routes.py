from flask import Blueprint, jsonify, request
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

contact_routes = Blueprint("contact_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@contact_routes.route("/api/contact_university", methods=["POST"])
def contact_university():
    data = request.get_json()
    university = data.get("university")
    message = data.get("message")

    if not university or not message:
        return jsonify({"error": "Missing data"}), 400

    try:
        supabase.table("university_messages").insert({
            "university": university,
            "message": message
        }).execute()
        return jsonify({"message": f"Message sent successfully to {university}!"})
    except Exception as e:
        print("Error saving message:", e)
        return jsonify({"error": "Server error"}), 500
