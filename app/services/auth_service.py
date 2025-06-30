from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token
from datetime import timedelta


def authenticate_user(db: Session, email: str, password: str):
    # Récupère l'utilisateur par son email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    # Vérifie si le mot de passe correspond
    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        return None

    # Si ok, crée le token JWT
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }
