import pytest
from backend.routes.login_routes import login_routes
from flask import Flask
from supabase import create_client, Client
from postgrest import APIError

SUPABASE_URL="https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(login_routes)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

usuarios = supabase.table("users").select("*").execute()

def test_user_register_new_user(client):
    response = client.post("/api/register", json={
        "name": "sofia",
        "email": "sofia@gmail.com",
        "password_hash": "1234"})
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully."
    supabase.table("users").delete().eq("email", "sofia@gmail.com").execute()
    
def test_user_register_existing_user(client):
    response = client.post("/api/register", json={
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "password_hash": "hashed_password_123"})
    assert response.status_code == 400
    assert response.json["message"] == "User already registered."

def test_user_login_success(client):
    response = client.get("/api/login", json={
        "email": "alice@example.com",
        "password": "hashed_password_123"})
    assert response.status_code == 200
    assert response.json["message"] == "Login successful."

def test_user_login_wrong_password(client):
    response = client.get("/api/login", json={
        "email": "alice@example.com",
        "password": "wrong"})
    assert response.status_code == 401
    assert response.json["message"] == "Invalid salt"

def test_user_login_nonexistent_user(client):
    response = client.get("/api/login", json={
        "email": "pepe2442424@gmail.com",
        "password": "1234"})
    assert response.status_code == 401
    assert response.json["message"] == "User is not registered"