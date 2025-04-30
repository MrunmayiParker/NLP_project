from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
# from app.routes.upload import upload_bp
# from app.routes.chat import chat_bp
# from app import db #change

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="../templates", instance_relative_config=True) # instance_relative_config - Lets you load config from the instance/ folder, which is not version-controlled
    
    # Loads configuration class (Config) from instance/config.py
    app.config.from_object("instance.config.Config")
    
    # Binds the extensions to the Flask app instance.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # CORS(app, supports_credentials=True)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    login_manager.login_view = 'auth.login' 

    with app.app_context():
        from app.models import user, paper, conversation, conversation_session

        from app.routes.auth import auth_bp
        from app.routes.chat import chat_bp
        from app.routes.upload import upload_bp
        from app.routes.home import main_bp
        from app.routes.search import search_bp
        from app.routes.search_chat import search_ui_bp 
        
        
        app.register_blueprint(search_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(chat_bp)
        app.register_blueprint(upload_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(search_ui_bp)

        @login_manager.user_loader
        def load_user(user_id):
            from app.models.user import User
            return User.query.get(int(user_id))

    return app
