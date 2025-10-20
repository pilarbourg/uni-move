from flask import Blueprint, jsonify, request
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

bio_profile_routes = Blueprint("bio_profile_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@bio_profile_routes.route("/api/get_biomedical_profile", methods=["GET"])
def get_biomedical_profile():
    user_id = 115  # TEMPORARY for testing

    response = supabase.table("biomedical_profiles") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    profiles = response.data or []
    if not profiles:
        return jsonify({"message": "No biomedical profile found"}), 404

    profile = profiles[0]

    illness_links = supabase.table("biomedical_profile_illnesses") \
        .select("illness_id") \
        .eq("biomedical_profile_id", profile["id"]) \
        .execute()

    illness_ids = [row["illness_id"] for row in illness_links.data or []]

    illnesses = []
    if illness_ids:
        illnesses_res = supabase.table("illnesses") \
            .select("id, name") \
            .in_("id", illness_ids) \
            .execute()
        illnesses = illnesses_res.data or []

    protocols = []
    if illness_ids:
        protocols_res = supabase.table("protocols") \
            .select("illness_id, step_order, instruction") \
            .in_("illness_id", illness_ids) \
            .order("step_order") \
            .execute()
        protocols = protocols_res.data or []

    profile["illnesses"] = illnesses
    profile["protocols"] = protocols

    contacts_res = (
        supabase.table("medical_contacts")
        .select("id, name, phone, email")
        .eq("biomedical_profile_id", profile["id"])
        .order("id", desc=True)
        .execute()
    )

    profile["contacts"] = contacts_res.data or []

    return jsonify(profile)


@bio_profile_routes.route("/api/post_biomedical_profile", methods=["POST"])
def post_biomedical_profile():
    user_id = 115  # TEMPORARY for testing
    data = request.json

    existing_profile = supabase.table("biomedical_profiles") \
        .select("*") \
        .eq("user_id", user_id) \
        .maybe_single() \
        .execute()

    if existing_profile and existing_profile.data:
        return jsonify({"message": "Biomedical profile already exists"}), 409

    new_profile = {
        "user_id": user_id,
        "allergies": data.get("allergies"),
        "weight": data.get("weight"),
        "height_cm": data.get("height_cm"),
    }

    response = supabase.table("biomedical_profiles").insert(new_profile).execute()
    if not response.data:
        return jsonify({"message": "Failed to create biomedical profile"}), 400

    created_profile = response.data[0]

    illness_ids = data.get("illnesses", [])
    if illness_ids:
        inserts = [
            {"biomedical_profile_id": created_profile["id"], "illness_id": int(ill)}
            for ill in illness_ids
        ]
        supabase.table("biomedical_profile_illnesses").insert(inserts).execute()

    illness_names = []
    if illness_ids:
        ill_res = supabase.table("illnesses").select("id, name").in_("id", illness_ids).execute()
        illness_names = ill_res.data or []

    created_profile["illnesses"] = illness_names

    return jsonify({"profile": created_profile}), 201
