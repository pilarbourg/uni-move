from flask import Blueprint, jsonify, request
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

related_degrees_routes = Blueprint("related_degrees_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@related_degrees_routes.route("/get_related_degrees", methods=["GET"])
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

        if not response.data:
            return jsonify({"related_degrees": []})

        similar_text = response.data[0].get("similar_degrees", "")
        similar_list = [s.strip() for s in similar_text.split(",") if s.strip()]

        return jsonify({"related_degrees": similar_list})

    except Exception as e:
        print(" Error fetching related degrees:", e)
        return jsonify({"error": "Internal server error"}), 500
