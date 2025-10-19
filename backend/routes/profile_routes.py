import re
from supabase import create_client, Client
from flask import Blueprint, jsonify, request

profile_routes = Blueprint("profile_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class User:
    def __init__(self, name, nationality, hobby):
        self.name = name
        self.nationality = nationality
        self.hobby = hobby

    def to_dict(self):
        return {
            "name": self.name,
            "nationality": self.nationality,
            "hobby": self.hobby
        }
    
@profile_routes.route("/api/registerprofile", methods=["POST"])
def user_register_profile():
    data = request.json
    name = data.get("name")
    nationality = data.get("nationality")
    hobby = data.get("hobby")

    if not all([name, nationality, hobby]):
        return jsonify({"message": "Missing required fields"}), 400
    
    if re.search(r'\d', name):
        return jsonify({"message": "Invalid name format."}), 201

    new_profile = User(name, nationality, hobby)
    supabase.table("profile").insert(new_profile.to_dict()).execute()

    return jsonify({"message": "User registered successfully."}), 200