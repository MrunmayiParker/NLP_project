from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True) # instance_relative_config - Lets you load config from the instance/ folder, which is not version-controlled
    
    # Loads configuration class (Config) from instance/config.py
    app.config.from_object("instance.config.Config")
    
    # Binds the extensions to the Flask app instance.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.upload import upload_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(upload_bp)

    return app
