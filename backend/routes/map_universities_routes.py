from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client


load_dotenv()

map_universities_routes = Blueprint("map_universities_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@map_universities_routes.route("/get_universities", methods=["GET"])
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

@map_universities_routes.route("/get_degrees", methods=["GET"])
def get_degrees():
    response = supabase.table("degrees").select("*").execute()

    degrees = [
        {
            "id": d.get("id"),
            "name": d.get("name"),

        }
        for d in response.data
    ]

    if degrees is None:
        # Something went wrong
        return jsonify({"error": "Could not fetch degrees"}), 500

    return jsonify(degrees)

@map_universities_routes.route("/get_universities_by_degree/<int:degree_id>", methods=["GET"])
def get_universities_by_degree(degree):
    query = f"""
        SELECT u.id, u.name, u.latitude, u.longitude, d.name as degree
        FROM universities u
        JOIN university_degrees ud ON u.id = ud.university_id
        JOIN degrees d ON d.id = ud.degree_id
        WHERE d.name = '{degree}'
    """
    data = supabase.rpc("execute_sql", {"sql": query}).execute()
    return jsonify(data.data)