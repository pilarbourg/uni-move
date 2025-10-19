from flask import Blueprint, jsonify, request
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

related_degrees_routes = Blueprint("related_degrees_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@related_degrees_routes.route("/api/get_related_degrees", methods=["GET"])
def get_related_degrees():
    degree = request.args.get("degree")

    if not degree:
        return jsonify({"error": "Missing parameter 'degree'"}), 400

    try:
        response = (
            supabase.table("degrees")
            .select("similar_degrees")
            .ilike("name", degree)
            .execute()
        )

        if not response.data or not response.data[0]["similar_degrees"]:
            return jsonify({"related_degrees": []})

        similar_str = response.data[0]["similar_degrees"]
        related_list = [d.strip() for d in similar_str.split(",")]
        return jsonify({"related_degrees": related_list})
    except Exception as e:
        print("Error in get_related_degrees:", e)
        return jsonify({"error": "Internal server error"}), 500
