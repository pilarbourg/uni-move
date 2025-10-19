from flask import Blueprint, jsonify
import requests
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

libraries_routes = Blueprint("libraries_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@libraries_routes.route("/api/libraries")
def get_libraries():
    response = supabase.table("libraries").select("*").execute()
    return jsonify(response.data)