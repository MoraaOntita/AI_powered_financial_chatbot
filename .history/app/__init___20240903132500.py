from flask import Flask
from app.services.chatbot import chatbot_bp

class AppInitializationError(Exception):
    """Custom exception for application initialization errors."""
    pass

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from environment variables or default settings
    app.config.from_object('config.Config')  # Adjust as needed based on your config setup

    # Register blueprints
    try:
        app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    except ImportError as e:
        raise AppInitializationError(f"Failed to initialize the app: {e}")

    # Initialize other extensions and middleware if needed
    # For example, database initialization, error handling, etc.

    return app
