from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db
from app.services.auth_service import login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    db: Session = next(get_db())
    data = request.get_json()

    # Check if required fields are present
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]

    # Try to login the user
    result = login_user(db, email, password)

    if not result:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(result)
