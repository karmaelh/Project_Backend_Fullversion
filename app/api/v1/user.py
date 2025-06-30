from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, login_required
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

# Create a new user
@bp.route('/', methods=['POST'])
def create_user():
    db: Session = next(get_db())
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    try:
        user_data = UserCreate(**data)
        hashed_password = get_password_hash(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Get all users
@bp.route('/', methods=['GET'])
def get_users():
    db: Session = next(get_db())
    users = db.query(User).all()
    users_list = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
    return jsonify(users_list)


# Get a single user
@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db: Session = next(get_db())
    user = db.query(User).get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'error': 'User not found'}), 404


# Update a user
@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db: Session = next(get_db())
    user = db.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    try:
        db.commit()
        db.refresh(user)
        return jsonify({'message': 'User updated successfully', 'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a user
@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db: Session = next(get_db())
    user = db.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        db.delete(user)
        db.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

# Protected route: get current user
@bp.route('/me', methods=['GET'])
@login_required
def read_users_me(user):
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })