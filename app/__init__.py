from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import logging
from config import DB_CONFIG

class AppInitializationError(Exception):
    """Custom exception for errors during app initialization."""
    pass

db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    try:
        # Load secret key from environment variable or default value
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

        # Load database configuration from environment variables
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        migrate.init_app(app, db)
        CORS(app)

        # Register your blueprints here
        from app.routes.index import index_bp
        app.register_blueprint(index_bp)

        # Ensure chatbot_bp is imported from the correct module
        from app.services.chatbot import chatbot_bp
        app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

        return app

    except ImportError as e:
        logging.error(f"Import error: {e}")
        raise AppInitializationError(f"Failed to initialize the app due to import error: {e}")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise AppInitializationError(f"Failed to initialize the app: {e}")
