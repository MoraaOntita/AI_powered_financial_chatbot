from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from typing import Optional

db = SQLAlchemy()
migrate = Migrate()

class AppInitializationError(Exception):
    """Custom exception for errors during app initialization."""
    pass

def create_app(config_object: Optional[str] = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_object (Optional[str]): The Python path of the config object, 
                                       e.g. 'config.Config'. If None, uses the default config.

    Returns:
        Flask: The configured Flask application instance.
    
    Raises:
        AppInitializationError: If there is an error during app initialization.
    """
    try:
        app = Flask(__name__)

        if config_object:
            app.config.from_object(config_object)
        else:
            from config import Config
            app.config.from_object(Config)

        # Initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        CORS(app)

        # Register blueprints
        from app.routes.index import main_bp
        app.register_blueprint(main_bp)

        return app

    except Exception as e:
        raise AppInitializationError(f"Failed to initialize the app: {e}")

