from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, login_required
from app.services.auth_service import login_user
from app.models.user import User
from app.core.security import get_password_hash

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



@auth_bp.route('/reset-password', methods=['PUT'])
def reset_password():
    db = next(get_db())
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return jsonify({"message": "Password updated successfully"})




