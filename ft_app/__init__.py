import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from ft_app.models.models import User, BodyWeightRecord


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

    from .models.dbc.database import init_db
    init_db()
    populate_dbc()

    @app.route('/')
    def index():
        return render_template("index.html")

    from . import bw_tracker
    app.register_blueprint(bw_tracker.bp)
    app.add_url_rule('/', endpoint='index')

    from . import exercises
    app.register_blueprint(exercises.bp)

    from . import training_planner
    app.register_blueprint(training_planner.bp)

    from . import personal_trainers
    app.register_blueprint(personal_trainers.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import about
    app.register_blueprint(about.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app


def populate_dbc():
    from ft_app.models.dbc.database import db_session
    if not User.query.all():
        db_session.add(User(username="Adrian", password="123", email="<ceo@zf.com>"))
        db_session.add(User(username="Ganesh", password="Ganesh", email="<ganesh@zf.com>"))

        db_session.add(BodyWeightRecord(weight=90.5, date="2023-01-01"))
        db_session.add(BodyWeightRecord(weight=91.2, date="2023-01-02"))
        db_session.add(BodyWeightRecord(weight=92.5, date="2023-01-03"))
        db_session.add(BodyWeightRecord(weight=95.5,  date="2023-01-04"))
        db_session.commit()
