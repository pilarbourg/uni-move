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
    def user_register(self,name,email,password):
        user_register = User(name,email,password)
        if user_register.email in usuarios:
            return jsonify({"message": "User already registered."}), 200
        #futuro hash
        #hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        #password_hash_str = hashed.decode("utf-8")
        supabase.table("users").insert({"name": user_register.name,"email": user_register.email,"password_hash": user_register.password}).execute()