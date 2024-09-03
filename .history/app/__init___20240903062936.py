from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    from app.routes.index import index_bp
    app.register_blueprint(index_bp)
    return app