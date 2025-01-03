from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # You can initialize extensions here (e.g., database, caching)

    # Register blueprints (if you're using them)
    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
