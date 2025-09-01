from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.api.v1 import user, auth
from app.core.config import load_config
from app.db.session import db  
from app.upload import upload_bp

migrate = Migrate() 
def create_app():
    app = Flask(__name__)
    load_config(app)

    db.init_app(app)        
    migrate.init_app(app, db) 

    #CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:57499"], supports_credentials=True)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:*"]}}, supports_credentials=True)


    app.register_blueprint(user.bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth.auth_bp, url_prefix='/api/v1/auth')

    app.register_blueprint(upload_bp)

    return app






