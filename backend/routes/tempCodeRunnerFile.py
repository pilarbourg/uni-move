    profile = existing_profile.data
    if profile is not None:
        return jsonify({"message": "Biomedical profile already exists"}), 409