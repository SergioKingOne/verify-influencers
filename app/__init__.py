from flask import Flask
from config import Config
from app.utils.logger import setup_logger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup logging
    logger = setup_logger(app)
    logger.info("Application startup")

    # Register blueprints
    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
