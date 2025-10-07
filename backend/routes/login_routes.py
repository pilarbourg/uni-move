from supabase import create_client, Client
from flask import Blueprint, jsonify, request

login_routes = Blueprint("login_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password
        }

@login_routes.route("/api/login", methods=["GET"])
def user_login():
    data = request.get_json(silent=True) or {}
    email = request.args.get("email") or data.get("email")
    password = request.args.get("password") or data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    result = supabase.table("users").select("*").eq("email", email).execute()
    users = result.data

    if not users:
        return jsonify({"message": "User is not registered"}), 401

    user = users[0]

    if user["password_hash"] == password:
        return jsonify({"message": "Login successful."}), 200

    return jsonify({"message": "Invalid salt"}), 401

@login_routes.route("/api/register", methods=["POST"])
def user_register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password_hash")

    if not all([name, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    existing_users = supabase.table("users").select("*").eq("email", email).execute()

    if existing_users.data:
        return jsonify({"message": "User already registered."}), 400

    new_user = User(name, email, password)
    supabase.table("users").insert(new_user.to_dict()).execute()

    return jsonify({"message": "User registered successfully."}), 201
