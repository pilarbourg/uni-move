from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

moving_routes = Blueprint("moving_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
ORS_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjAzNjA1M2RiMGZjYzQyZGFhZmYyMGU4ZWZjNTkwZmE3IiwiaCI6Im11cm11cjY0In0="  # OpenRouteService API Key

@moving_routes.route("/get_moving_companies", methods=["GET"])
def get_moving_companies():
    response = supabase.table("moving_companies").select("*").execute()

    companies = [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "cif": c.get("cif"),
            "base_fee": c.get("base_fee"),
            "price_small_package": c.get("price_small_package"),
            "price_medium_package": c.get("price_medium_package"),
            "price_large_package": c.get("price_large_package"),
            "price_solo_traslado": c.get("price_solo_traslado"),
            "price_mudanza": c.get("price_mudanza"),
            "price_mudanza_completa": c.get("price_mudanza_completa"),
            "rating": c.get("rating"),
            "location": c.get("location"),
            "estimated_time_days": c.get("estimated_time_days"),
            "max_weight_kg": c.get("max_weight_kg"),

            
        }
        for c in response.data
    ]

    if companies is None:
        # Something went wrong
        return jsonify({"error": "Could not fetch companies"}), 500

    return jsonify(companies)

@moving_routes.route("/calc_distance")
def calc_distance():
    origin = request.args.get("from", "")
    destination = request.args.get("to", "")

    if not origin or not destination:
        return jsonify({"error": "Missing parameters"}), 400

    # 1 — Geocode ORIGIN
    geo_url_o = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={origin}"
    res_o = requests.get(geo_url_o).json()
    if not res_o.get("features"):
        return jsonify({"error": "Invalid origin"}), 400

    lon_o, lat_o = res_o["features"][0]["geometry"]["coordinates"]

    # 2 — Geocode DESTINATION
    geo_url_d = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={destination}"
    res_d = requests.get(geo_url_d).json()
    if not res_d.get("features"):
        return jsonify({"error": "Invalid destination"}), 400

    lon_d, lat_d = res_d["features"][0]["geometry"]["coordinates"]

    # 3 — Calculate route distance
    directions_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    payload = {
        "coordinates": [
            [lon_o, lat_o],
            [lon_d, lat_d]
        ]
    }
    headers = {
        "Authorization": ORS_KEY,
        "Content-Type": "application/json"
    }

    route_res = requests.post(directions_url, json=payload, headers=headers).json()

    try:
        distance_m = route_res["routes"][0]["summary"]["distance"]
        distance_km = round(distance_m / 1000, 1)

        return jsonify({"distance_km": distance_km})

    except Exception as e:
        return jsonify({"error": "Routing failed", "details": str(e)}), 500


@moving_routes.route("/validate_address")
def validate_address():
    city = request.args.get("city")
    import requests

    url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={city}"
    res = requests.get(url).json()

    exists = len(res.get("features", [])) > 0

    return jsonify({"valid": exists})

