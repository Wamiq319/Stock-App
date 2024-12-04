from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Register the blueprint as routes_blueprint
    from .routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)
    
    return app
