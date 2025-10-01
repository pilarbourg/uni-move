from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

bio_profile_routes = Blueprint("bio_profile_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@bio_profile_routes.route("/api/get_biomedical_profile", methods=["GET"])
def get_biomedical_profile():
    user_id = 6  # TESTING

    response = supabase.table("biomedical_profiles")\
        .select("*")\
        .eq("user_id", user_id)\
        .execute()

    if response.data and len(response.data) > 0:
        return jsonify(response.data[0])
    else:
        return jsonify({"message": "No biomedical profile found"}), 404
    
@bio_profile_routes.route("/api/post_biomedical_profile", methods=["POST"])
def post_biomedical_profile():
    user_id = 6  # TESTING
    data = request.json

    user_check = supabase.table("users").select("*").eq("id", user_id).maybe_single().execute()
    print("DEBUG user_check:", user_check)

    if not user_check or not getattr(user_check, "data", None):
        return jsonify({"message": "User does not exist"}), 404

    existing_profile = supabase.table("biomedical_profiles").select("*").eq("user_id", user_id).maybe_single().execute()

    if existing_profile and getattr(existing_profile, "data", None):
        return jsonify({"message": "Biomedical profile already exists"}), 409

    new_profile = {
        "user_id": user_id,
        "allergies": data.get("allergies"),
        "illnesses": data.get("illnesses"),
        "weight": data.get("weight"),
        "height_cm": data.get("height_cm"),
    }

    response = supabase.table("biomedical_profiles").insert(new_profile).execute()

    if response and response.data:
        return jsonify(response.data[0]), 201
    else:
        return jsonify({"message": "Failed to create biomedical profile"}), 400
    