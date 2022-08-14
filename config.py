import os
SECRET_KEY = os.urandom(32)  # For initialize flask-wtforms
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/flasky"
SQLALCHEMY_TRACK_MODIFICATIONS = False
