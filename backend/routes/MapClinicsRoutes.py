from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import math
import os
from supabase import create_client

app = Flask(__name__) 
CORS(app)

load_dotenv()

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


@app.route("/universities", methods=["GET"])
def get_universities():
    response = supabase.table("universities").select("*").execute()

    if response.error:
        return jsonify({"error": response.error.message}), 500

    universities = [
        {
            "id": u.get("id"),
            "name": u.get("name"),
            "latitude": u.get("latitude"),
            "longitude": u.get("longitude"),
        }
        for u in response.data
    ]
    return jsonify(universities)


@app.route("/universities/<int:university_id>/clinics", methods=["GET"])
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


if __name__ == "__main__":
    app.run(debug=True)