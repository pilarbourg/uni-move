from flask import Blueprint, jsonify, request
from backend.university_info.university_details import UniversityDetail, DegreeNotFoundException
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

university_search_routes = Blueprint("university_search_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@university_search_routes.route("/search_universities_by_degree", methods=["GET"])
def search_universities_by_degree():
    degree = request.args.get("degree")

    if not degree:
        return jsonify({"error: Missing parameter 'degree"}), 400

    try:
        response = (
            supabase.table("universities")
            .select("id, name, ranking, publicTransport, zipCode, phoneNumber")
            .ilike("faculty_type", f"%{degree}%")
            .execute()
        )

        results = response.data

        if not results:
            raise DegreeNotFoundException(f"No universities were found for '{degree}'.")

        data = [
            {
                "id": u.get("id"),
                "name": u.get("name"),
                "ranking": u.get("ranking"),
                "publicTransport": u.get("publicTransport"),
                "zipCode": u.get("zipCode"),
                "phoneNumber": u.get("phoneNumber"),
            }
            for u in results
        ]

        return jsonify(data)

    except DegreeNotFoundException as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"Error: Internal server error"}), 500


@university_search_routes.route("/get_related_degrees", methods=["GET"])
def get_related_degrees():
    degree = request.args.get("degree")

    if not degree:
        return jsonify({"error": "Missing parameter 'degree'"}), 400

    try:
        degree_result = (
            supabase.table("degrees")
            .select("id")
            .ilike("name", degree)
            .execute()
        )

        if not degree_result.data:
            return jsonify({"related_degrees": []})

        degree_id = degree_result.data[0]["id"]

        related = (
            supabase.table("related_degrees")
            .select("related_id")
            .eq("degree_id", degree_id)
            .execute()
        )

        if not related.data:
            return jsonify({"related_degrees": []})

        related_ids = [r["related_id"] for r in related.data]

        related_names = (
            supabase.table("degrees")
            .select("name")
            .in_("id", related_ids)
            .execute()
        )

        names = [r["name"] for r in related_names.data]

        return jsonify({"related_degrees": names})

    except Exception as e:
        print("Error fetching related degrees:", e)
        return jsonify({"error": "Internal server error"}), 500