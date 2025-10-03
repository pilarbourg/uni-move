from flask import Blueprint, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

illness_routes = Blueprint("illness_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@illness_routes.route("/api/illnesses", methods=["GET"])
def get_illnesses():
    response = supabase.table("illnesses").select("id, name").execute()
    if response.data:
        return jsonify(response.data)
    else:
        return jsonify({"message": "No illnesses found"}), 404


@illness_routes.route("/api/protocols/<int:user_id>", methods=["GET"])
def get_protocols(user_id):
    profile = (
        supabase.table("biomedical_profiles")
        .select("illnesses")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not profile.data:
        return jsonify({"message": "No biomedical profile found"}), 404

    illness_ids_res = (
        supabase.table("biomedical_profile_illnesses")
        .select("illness_id")
        .eq("biomedical_profile_id", profile.data["id"])
        .execute()
    )
    illness_ids = [row["illness_id"] for row in (illness_ids_res.data or [])]

    if not illness_ids:
        return jsonify({"protocols": []})

    response = (
        supabase.table("protocols")
        .select("illness_id, step_order, instruction")
        .in_("illness_id", illness_ids)
        .order("step_order")
        .execute()
    )

    return jsonify(response.data)