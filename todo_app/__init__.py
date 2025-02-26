from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .auth_routes import auth
from .task_routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
