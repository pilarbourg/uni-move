from flask import Blueprint, request, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

libraries_reviews_routes = Blueprint("reviews_routes", __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BANNED_WORDS = ["suck my dick", "pito", "peno"] # BANNED WORDS

def sanitize_comment(comment):
    if not comment:
        return None
    for word in BANNED_WORDS:
        comment = comment.replace(word, "****")
    return comment

@libraries_reviews_routes.route("/api/libraries/<int:library_id>/reviews", methods=["POST"])
def add_review(library_id):
    data = request.json
    user_id = data.get("user_id")
    rating = data.get("rating")
    comment = sanitize_comment(data.get("comment"))

    if not user_id or not rating:
        return jsonify({"error": "Missing user_id or rating"}), 400

    response = supabase.table("libraries_reviews").insert({
        "library_id": library_id,
        "user_id": user_id,
        "rating": rating,
        "comment": comment
    }).execute()

    if response.error:
        return jsonify({"error": response.error.message}), 500

    return jsonify({"message": "Review added successfully", "review": response.data[0]})

@libraries_reviews_routes.route("/api/libraries/<int:library_id>/reviews", methods=["GET"])
def get_reviews(library_id):
    response = supabase.table("libraries_reviews").select("*").eq("library_id", library_id).execute()
    return jsonify(response.data)