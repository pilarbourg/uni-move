from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/api/get_biomedical_profile", methods=["GET"])
def get_biomedical_profile():
    # Hardcoded user_id for testing
    user_id = 1

    response = supabase.table("biomedical_profiles").select("*").eq("user_id", user_id).single().execute()

    if response.data:
        print(response.data)
        return jsonify(response.data)
    else:
        return jsonify({"message": "No biomedical profile found"}), 404
    
    # TODO POST ROUTE FOR WHEN FORM IS SUBMITTED

if __name__ == "__main__":
    app.run(debug=True)