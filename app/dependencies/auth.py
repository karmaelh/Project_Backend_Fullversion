from flask import request, jsonify
from jose import JWTError, jwt
from app.models.user import User
from app.db.session import SessionLocal
from app.core.config import settings
from functools import wraps

# JWT configuration
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Extract token from header and return the current user
def get_current_user():
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None  
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    db = next(get_db())
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        return f(user=user, *args, **kwargs)
    return decorated_function
