from supabase import create_client, Client
from flask import Blueprint, jsonify, request

login_routes = Blueprint("login_routes", __name__)

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "email": self.email,
            "password_hash": self.password
        }

@login_routes.route("/api/login", methods=["POST"])
def user_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    result = supabase.table("users").select("*").eq("email", email).execute()
    users = result.data

    if not users:
        return jsonify({"message": "User is not registered"}), 401

    user = users[0]

    if user["password_hash"] == password:
        # Verificar si el usuario ya tiene perfil completo
        has_profile = bool(user.get("profile_name") or user.get("nationality") or user.get("hobby"))
        
        return jsonify({
            "message": "Login successful.",
            "email": email,
            "success": True,
            "has_profile": has_profile,
            "profile_data": {
                "profile_name": user.get("profile_name"),
                "nationality": user.get("nationality"),
                "hobby": user.get("hobby")
            }
        }), 200

    return jsonify({"message": "Invalid password"}), 401

@login_routes.route("/api/register", methods=["POST"])
def user_register():
    data = request.json
    email = data.get("email")
    password = data.get("password_hash")

    if not all([email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    existing_users = supabase.table("users").select("*").eq("email", email).execute()

    if existing_users.data:
        return jsonify({"message": "User already registered."}), 400

    new_user = User(email, password)
    supabase.table("users").insert(new_user.to_dict()).execute()

    return jsonify({
        "message": "User registered successfully.",
        "email": email,
        "success": True,
        "has_profile": False
    }), 201

@login_routes.route("/api/check_profile/<email>", methods=["GET"])
def check_profile(email):
    """Endpoint para verificar si un usuario tiene perfil completo"""
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        
        if not result.data:
            return jsonify({"message": "User not found"}), 404
        
        user = result.data[0]
        has_profile = bool(user.get("profile_name") or user.get("nationality") or user.get("hobby"))
        
        return jsonify({
            "has_profile": has_profile,
            "profile_data": {
                "profile_name": user.get("profile_name"),
                "nationality": user.get("nationality"),
                "hobby": user.get("hobby")
            }
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500