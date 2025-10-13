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


