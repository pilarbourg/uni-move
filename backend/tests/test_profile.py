import pytest
from backend.routes.profile_routes import profile_routes
from flask import Flask
from supabase import create_client, Client
from postgrest import APIError

SUPABASE_URL="https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(profile_routes)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_user_register_new_profile(client):
    response = client.post("/api/registerprofile", json={
        "name": "Test User",
        "nationality": "Testland",
        "hobby": "Testing"})
    assert response.status_code == 200
    assert response.json["message"] == "User registered successfully."
    supabase.table("profile").delete().eq("name","Test User").execute()

def test_user_register_new_profile_wrong_format(client):
    response = client.post("/api/registerprofile", json={
        "name": "Test User32",
        "nationality": "Testland",
        "hobby": "Testing"})
    assert response.status_code == 201
    assert response.json["message"] == "Invalid name format."
    supabase.table("profile").delete().eq("name","Test User32").execute()