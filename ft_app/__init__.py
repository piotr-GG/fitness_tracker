import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fitness_tracker.sqlite')
    )
    if test_config is not None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Pozdrawiam Was, poczekacie!"

    from .models.dbc.database import init_db
    init_db()

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # db = SQLAlchemy(app)
    return app
