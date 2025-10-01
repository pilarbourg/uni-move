from flask import Blueprint, request, jsonify
from ..services.cohere_service import generate_text

chat_routes = Blueprint("chat_routes", __name__)

@chat_routes.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    result = generate_text(prompt)
    return jsonify({"response": result})