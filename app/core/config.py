import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./training.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-default-secret")

settings = Settings()

def load_config(app):
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
