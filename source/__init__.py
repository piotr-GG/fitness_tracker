from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db = SQLAlchemy(app)
    return app
