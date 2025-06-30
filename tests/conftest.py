import pytest
from app import create_app
from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    yield app

@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client()

@pytest.fixture(scope="module")
def test_user():
    db = SessionLocal()
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()
