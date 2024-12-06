from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()  # Initialize db instance here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the db with the app
    db.init_app(app)

    from .routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
