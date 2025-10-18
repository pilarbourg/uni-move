from flask import Blueprint, request, jsonify
from supabase import create_client
import os

medical_reminders_routes = Blueprint('medical_reminders_routes', __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@medical_reminders_routes.route('/api/post_medical_reminder', methods=['POST'])
def post_medical_reminder():
    data = request.get_json()

    biomedical_profile_id = data.get("biomedical_profile_id")
    contact_ids = data.get("contact_ids", [])
    message = data.get("message")

    if not (biomedical_profile_id and contact_ids and message):
        return jsonify({"error": "Missing required fields"}), 400

    reminders = []
    for cid in contact_ids:
        reminders.append({
            "biomedical_profile_id": biomedical_profile_id,
            "contact_id": cid,
            "message": message
        })

    try:
        response = supabase.table("medical_reminders").insert(reminders).execute()

        if not response.data:
            return jsonify({"error": "Failed to send the reminder"}), 400

        return jsonify({"message": "Reminders sent successfully"}), 200

    except Exception:
        return jsonify({"error": "Server error while sendint the reminder"}), 500
