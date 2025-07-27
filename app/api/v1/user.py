from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, login_required
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from transformers import pipeline
from datetime import date
import traceback
from datetime import datetime



summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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
            hashed_password=hashed_password,
            position=user_data.position,
            department=user_data.department,
            photoUrl=user_data.photoUrl,
            hire_date=user_data.hire_date,
            skills=user_data.skills,
            current_project=user_data.current_project,
            languages_spoken=user_data.languages_spoken 

        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'position': user.position,
                'department': user.department,
                'photoUrl': user.photoUrl,
                'hire_date': str(user.hire_date) if user.hire_date else None,
                'skills': user.skills,
                'current_project': user.current_project,
                'languages_spoken': user.languages_spoken

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
    users_list = [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'position': u.position,
        'department': u.department,
        'photoUrl': u.photoUrl,
        'hire_date': str(u.hire_date) if u.hire_date else None
    } for u in users]
    return jsonify(users_list)

# Get a single user
@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db: Session = next(get_db())
    user = db.query(User).get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'position': user.position,
            'department': user.department,
            'photoUrl': user.photoUrl,
            'hire_date': str(user.hire_date) if user.hire_date else None
        })
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
    if 'position' in data:
        user.position = data['position']
    if 'department' in data:
        user.department = data['department']
    if 'photoUrl' in data:
        user.photoUrl = data['photoUrl']
    if 'hire_date' in data:
        if data['hire_date']:  
            user.hire_date = datetime.strptime(data['hire_date'], "%Y-%m-%d").date()
        else:
            user.hire_date = None
    if 'skills' in data:
        user.skills = data['skills']
    if 'current_project' in data:
        user.current_project = data['current_project']
    if 'languages_spoken' in data:
        user.languages_spoken = data['languages_spoken']

    try:
        db.commit()
        db.refresh(user)
        return jsonify({'message': 'User updated successfully', 'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'position': user.position,
            'department': user.department,
            'photoUrl': user.photoUrl,
            'hire_date': str(user.hire_date) if user.hire_date else None,
            'skills': user.skills,
            'current_project': user.current_project,
            'languages_spoken': user.languages_spoken

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
        "email": user.email,
        "position": user.position,
        "department": user.department,
        "photoUrl": user.photoUrl,
        "hire_date": str(user.hire_date) if user.hire_date else None 

    })

@bp.route('/<int:user_id>/summary', methods=['GET'])
def generate_user_summary(user_id):
    db: Session = next(get_db())
    user = db.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    def format_hire_date(date_obj):
        try:
            return date_obj.strftime("%B %Y")  # ex: January 2025
        except:
            return "an unknown date"

    text = f"{user.username}, an {user.position or 'employee'} in the {user.department or 'team'} department at Thales, joined in {format_hire_date(user.hire_date)}."

    if user.current_project:
        text += f" {user.username.split()[0]} is currently working on {user.current_project}."

    if user.skills:
        text += f" They are experienced in {user.skills}."

    if user.languages_spoken:
        text += f" They speak {user.languages_spoken}."

    try:
        result = summarizer(text, max_length=60, min_length=25, do_sample=False)
        summary = result[0]['summary_text']
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
