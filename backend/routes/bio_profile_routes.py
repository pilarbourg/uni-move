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

    profiles = response.data or []
    if not profiles:
        return jsonify({"message": "No biomedical profile found"}), 404

    profile = profiles[0]  # get first profile

    illness_ids_res = (
        supabase.table("biomedical_profile_illnesses")
        .select("illness_id")
        .eq("biomedical_profile_id", profile["id"])
        .execute()
    )
    illness_ids = [row["illness_id"] for row in (illness_ids_res.data or [])]

    illnesses_res = []
    if illness_ids:
        illnesses_res = (
            supabase.table("illnesses")
            .select("id, name")
            .in_("id", illness_ids)
            .execute()
            .data
        )

    protocols_res = []
    if illness_ids:
        protocols_res = (
            supabase.table("protocols")
            .select("illness_id, step_order, instruction")
            .in_("illness_id", illness_ids)
            .order("step_order")
            .execute()
            .data
        )

    profile["illnesses"] = illnesses_res
    profile["protocols"] = protocols_res

    return jsonify(profile)


    
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
        "weight": data.get("weight"),
        "height_cm": data.get("height_cm"),
    }

    response = supabase.table("biomedical_profiles").insert(new_profile).execute()

    if not response or not response.data:
        return jsonify({"message": "Failed to create biomedical profile"}), 400

    created_profile = response.data[0]

    illness_ids = data.get("illnesses", [])
    if illness_ids:
        inserts = [
            {"biomedical_profile_id": created_profile["id"], "illness_id": int(ill)}
            for ill in illness_ids
        ]
        supabase.table("biomedical_profile_illnesses").insert(inserts).execute()

    created_profile["illnesses"] = resolve_illness_names(illness_ids)

    return jsonify({"profile": created_profile}), 201


#Obtain illnesses names from their ids
def resolve_illness_names(illness_ids):
    if not illness_ids:
        return []
    res = supabase.table("illnesses").select("id, name").in_("id", illness_ids).execute()
    return [ill["name"] for ill in res.data]