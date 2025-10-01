from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import math
import os
from supabase import create_client

load_dotenv()

map_clinics_routes = Blueprint("map_clinics_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# función Haversine para calcular distancia entre coordenadas en km
def haversine(latitude1, longitude1, latitude2, longitude2):
    R = 6371 
    dlatitude = math.radians(latitude2 - latitude1)
    dlongitude = math.radians(longitude2 - longitude1)
    a = math.sin(dlatitude / 2) ** 2 + math.cos(math.radians(latitude1)) \
        * math.cos(math.radians(latitude2)) * math.sin(dlongitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@map_clinics_routes.route("/universities", methods=["GET"])
def get_universities():
    response = supabase.table("universities").select("*").execute()

    universities = [
        {
            "id": u.get("id"),
            "name": u.get("name"),
            "latitude": u.get("latitude"),
            "longitude": u.get("longitude"),
        }
        for u in response.data
    ]

    if universities is None:
        # Something went wrong
        return jsonify({"error": "Could not fetch universities"}), 500

    return jsonify(universities)


@map_clinics_routes.route("/universities/<int:university_id>/clinics", methods=["GET"])
def get_clinics(university_id):
    radius = float(request.args.get("radius", 2))

    # 1. obtain universities from supabase
    uni_response = supabase.table("universities") \
        .select("id, name, latitude, longitude") \
        .eq("id", university_id) \
        .single() \
        .execute()

    if not uni_response.data:
        return jsonify({"error": "Universidad no encontrada"}), 404
    
    university = uni_response.data
    uni_latitude, uni_longitude = university["latitude"], university["longitude"]

    #2. obtain clinics from supabase
    clinics_response = supabase.table("clinics") \
        .select("id, name, latitude, longitude") \
        .execute()

    if not clinics_response.data:
        return jsonify([])

    #3. apply radius
    nearby_clinics = []
    for clinic in clinics_response.data:
        distance_km = haversine(uni_latitude, uni_longitude, clinic["latitude"], clinic["longitude"])
        if distance_km <= radius:
            nearby_clinics.append({
                "id": clinic["id"],
                "name": clinic["name"],
                "latitude": clinic["latitude"],
                "longitude": clinic["longitude"],
                "distance_km": round(distance_km, 2)
            })
    
    nearby_clinics= sorted(nearby_clinics, key = lambda x: x["distance_km"])
    return jsonify(nearby_clinics)


@map_clinics_routes.route("/universities", methods=["POST"])
def create_university():
    """
    Create a new university. Expects JSON body:
    {
        "name": "University Name",
        "latitude": 40.4168,
        "longitude": -3.7038
    }
    """
    data = request.get_json()

    # Validate required fields
    if not data or not all(k in data for k in ("name", "latitude", "longitude")):
        return jsonify({"error": "Missing required fields: name, latitude, longitude"}), 400

    new_uni = {
        "name": data["name"],
        "latitude": data["latitude"],
        "longitude": data["longitude"]
    }

    try:
        response = supabase.table("universities").insert(new_uni).execute()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not response.data:
        return jsonify({"error": "Could not create university"}), 500

    return jsonify(response.data[0]), 201  # Return the created university with status 201


if __name__ == "__main__":
    app.run(debug=True)