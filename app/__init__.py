import logging
import colorlog
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

import logging
import colorlog

def setup_logger(name: str) -> logging.Logger:
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    ))
    
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    
    # Set the level for your custom logger, not the global logger
    logger.setLevel(logging.DEBUG)
    
    return logger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logger = setup_logger("app_logger")

    db.init_app(app)

    from .routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    logger.info("App started successfully!")

    return app
