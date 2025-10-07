from flask import Blueprint, jsonify, request
from backend.university_info.university_details import UniversityDetail, DegreeNotFoundException

university_search_routes = Blueprint("university_search_routes", __name__)

@university_search_routes.route("/search_universities_by_degree", methods=["GET"])
def search_universities_by_degree():
    degree = request.args.get("degree")

    if not degree:
        return jsonify({"error": "Falta el parámetro 'degree'"}), 400

    try:
        results = UniversityDetail.search_by_degree(degree)
        data = [
            {
                "id": u.id,
                "name": u.name,
                "ranking": u.ranking,
                "publicTransport": u.public_transport,
                "zipCode": u.zip_code,
                "phoneNumber": u.phone,
            }
            for u in results
        ]
        return jsonify(data)

    except DegreeNotFoundException as e:
        return jsonify({"error": str(e)}), 404
