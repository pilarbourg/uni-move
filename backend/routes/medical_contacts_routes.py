from flask import Blueprint, jsonify, request
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

medical_contacts_routes = Blueprint("medical_contacts_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BIOMEDICAL_ID = 11 # TEMPORARY biomedical_profiles_id for testing

@medical_contacts_routes.route("/api/medical_contacts", methods=["GET"])
def get_medical_contacts():
    try:
        response = (
            supabase.table("medical_contacts")
            .select("*")
            .eq("biomedical_profile_id", BIOMEDICAL_ID)
            .order("id", desc=True)
            .execute()
        )

        return jsonify(response.data or []), 200
    except Exception:
        return jsonify({"error": "Failed to fetch contacts"}), 500

@medical_contacts_routes.route("/api/medical_contacts", methods=["POST"])
def add_medical_contact():
    data = request.json
    
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    new_contact = {
        "biomedical_profile_id": BIOMEDICAL_ID,
        "name": data.get("name"),
        "phone": data.get("phone"),
        "email": data.get("email"),
    }

    try:
        response = supabase.table("medical_contacts").insert(new_contact).execute()

        if not response.data:
            return jsonify({"error": "Failed to insert contact"}), 400

        return jsonify(response.data[0]), 201

    except Exception:
        return jsonify({"error": "Server error while adding contact"}), 500


@medical_contacts_routes.route("/api/medical_contacts/<int:contact_id>", methods=["PUT"])
def update_medical_contact(contact_id):
    data = request.json

    updated_contact = {
        "name": data.get("name"),
        "phone": data.get("phone"),
        "email": data.get("email"),
    }

    try:
        response = supabase.table("medical_contacts") \
            .update(updated_contact) \
            .eq("id", contact_id) \
            .eq("biomedical_profile_id", BIOMEDICAL_ID) \
            .execute()

        if not response.data:
            return jsonify({"error": "Update failed"}), 400

        return jsonify(response.data[0]), 200
    except Exception:
        return jsonify({"error": "Server error while updating contact"}), 500

@medical_contacts_routes.route("/api/medical_contacts/<int:contact_id>", methods=["DELETE"])
def delete_medical_contact(contact_id):
    try:
        response = supabase.table("medical_contacts") \
            .delete() \
            .eq("id", contact_id) \
            .eq("biomedical_profile_id", BIOMEDICAL_ID) \
            .execute()

        if response.error:
            return jsonify({"error": response.error.message}), 400

        return jsonify({"message": "Contact deleted"}), 200
    except Exception:
        return jsonify({"error": "Server error while deleting contact"}), 500
