import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./training.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-default-secret")
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER") or os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../uploads')


settings = Settings()

def load_config(app):
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
