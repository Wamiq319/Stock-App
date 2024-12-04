import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stocks.db'  # SQLite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
