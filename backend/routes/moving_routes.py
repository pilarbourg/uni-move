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

@moving_routes.route("/calc_distance", methods=["GET"])
def calc_distance(cityA, cityB):
    import requests
    # 1. Geocode city A
    urlA = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={cityA}"
    dataA = requests.get(urlA).json()
    coordA = dataA["features"][0]["geometry"]["coordinates"]

    # 2. Geocode city B
    urlB = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={cityB}"
    dataB = requests.get(urlB).json()
    coordB = dataB["features"][0]["geometry"]["coordinates"]

    lon1, lat1 = coordA
    lon2, lat2 = coordB

    # 3. Distance request
    urlD = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_KEY}&start={lon1},{lat1}&end={lon2},{lat2}"
    distData = requests.get(urlD).json()

    meters = distData["features"][0]["properties"]["summary"]["distance"]
    km = round(meters / 1000, 2)

    return jsonify({"distance_km": km})

@moving_routes.route("/validate_address")
def validate_address(city):
    import requests

    url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_KEY}&text={city}"
    res = requests.get(url).json()

    exists = len(res.get("features", [])) > 0

    return jsonify({"valid": exists})

