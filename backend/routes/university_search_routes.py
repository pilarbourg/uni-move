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


@university_search_routes.route("/api/search_universities_by_degree", methods=["GET"])
def search_universities_by_degree():
    degree = request.args.get("degree")
    uni_type = request.args.get("type")
    rank_filter = request.args.get("ranking")

    if not degree:
        return jsonify({"error": "Missing parameter 'degree'"}), 400

    try:
        # Base query
        query = (
            supabase.table("universities")
            .select("id, name, ranking, publicTransport, zipCode, phoneNumber, type")
            .ilike("faculty_type", f"%{degree}%")
        )

        if uni_type:
            query = query.eq("type", uni_type.lower())

        if rank_filter == "1-10":
            query = query.gte("ranking", 1).lte("ranking", 10)
        elif rank_filter == "11-20":
            query = query.gte("ranking", 11).lte("ranking", 20)
        elif rank_filter == "21-50":
            query = query.gte("ranking", 21).lte("ranking", 50)

        query = query.neq("ranking", 0)

        response = query.execute()
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
                "type": u.get("type"),
            }
            for u in results
        ]

        return jsonify(data)

    except DegreeNotFoundException as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500