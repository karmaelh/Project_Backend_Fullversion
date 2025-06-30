from flask import Flask
from app.api.v1 import user, auth
from app.core.config import load_config


def create_app():
    app = Flask(__name__)
    load_config(app)

    # Register the user blueprint
    app.register_blueprint(user.bp, url_prefix='/api/v1/users')

    # Register the auth blueprint 
    app.register_blueprint(auth.auth_bp, url_prefix='/api/v1/auth')

    return app
