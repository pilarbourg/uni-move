from supabase import create_client, Client
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import bcrypt

load_dotenv()
login_routes = Blueprint("login_routes", __name__)
SUPABASE_URL="https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
usuarios = supabase.table("users").select("*").execute()

class User:
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
@login_routes.route("/api/login", methods=["GET"])
def user_login(self,email,password):
        emails = supabase.table("users").select("*").eq("email", email).execute().data
        if not emails:
            return jsonify({"message": "User is not registered."}), 200
        user = emails[0]
        if user["password_hash"] == password:
            return True
        return jsonify({"message": "Invalid salt."}), 200
        #futuro hash
        #stored_hash = user["password_hash"].encode("utf-8")
        #if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        #    return True
        #else:
        #    raise ValueError("Wrong password")
@login_routes.route("/api/register", methods=["POST"])
def user_register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password_hash")

    new_user = User(name, email, password)

    existing_users = supabase.table("users").select("*").eq("email", new_user.email).execute()

    if existing_users.data:
        return jsonify({"message": "User already registered."}), 400
    
    #futuro hash
    #hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    #password_hash_str = hashed.decode("utf-8")
        
    supabase.table("users").insert({"name": new_user.name,"email": new_user.email,"password_hash": new_user.password}).execute()

    #todo --> confirm that user is created with hashed password
    return jsonify({"message": "User registered successfully."}), 201