from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from ..services.supabase_client import supabase

load_dotenv()

map_universities_routes = Blueprint("map_universities_routes", __name__, url_prefix="/api")

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
        return jsonify({"error": "Could not fetch degrees"}), 500

    return jsonify(degrees)

@map_universities_routes.route("/get_locations", methods=["GET"])
def get_locations():
    response = supabase.table("localities").select("*").execute()

    locations = [
        {
            "id": l.get("id"),
            "name": l.get("name"),

        }
        for l in response.data
    ]

    if locations is None:
        return jsonify({"error": "Could not fetch locations"}), 500

    return jsonify(locations)

@map_universities_routes.route("/get_universities_by_degree/<int:degree>", methods=["GET"])
def get_universities_by_degree(degree):
    query = f"""
        SELECT u.id, u.name, u.latitude, u.longitude, u.ranking, u."publicTransport", u."zipCode", u."phoneNumber"
        FROM universities u
        JOIN university_degrees ud ON u.id = ud.university_id
        JOIN degrees d ON d.id = ud.degree_id
        WHERE d.id = '{degree}'
    """
    data = supabase.rpc("exec_sql", {"sql": query}).execute()
    return jsonify(data.data)

@map_universities_routes.route("/get_universities_by_degree_and_locality/<int:degree>/<int:location>", methods=["GET"])
def get_universities_by_degree_and_location(degree, location):
    query = f"""
        SELECT u.id, u.name, u.latitude, u.longitude, u.ranking, u."publicTransport", u."zipCode", u."phoneNumber"
        FROM universities u
        JOIN university_degrees ud ON u.id = ud.university_id
        JOIN degrees d ON d.id = ud.degree_id
        JOIN localities l ON u.locality_id = l.id
        WHERE d.id = '{degree}'
            AND l.id = '{location}'
    """
    data = supabase.rpc("exec_sql", {"sql": query}).execute()
    return jsonify(data.data)

@map_universities_routes.route("/get_universities_by_locality/<int:locality>", methods=["GET"])
def get_universities_by_locality(locality):
    query = f"""
        SELECT u.id, u.name, u.latitude, u.longitude, u.ranking, u."publicTransport", u."zipCode", u."phoneNumber"
        FROM universities u
        JOIN localities l ON u.locality_id = l.id
        WHERE l.id = '{locality}'
    """
    data = supabase.rpc("exec_sql", {"sql": query}).execute()
    return jsonify(data.data)