import datetime
import os
import random

from flask import Flask, render_template
from ft_app.dbc.database import DBC


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fitness_tracker.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        DBC.init_db()

    if not app.config.get("TESTING"):
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
    from ft_app.dbc.database import DBC
    from ft_app.models import User, BodyWeightRecord, BlogPost

    db_session = DBC.get_db_session()

    if not db_session.query(User).all():
        db_session.add(User(username="admin_123", password="admin_123", email="admin_123@ft.com", is_moderator=True))
        db_session.add(User(username="ganesh", password="ganesh", email="ganesh@gmail.com"))
        db_session.add(User(username="adrian_123", password="adrian_123", email="adrian_123@gmail.com"))
        db_session.add(User(username="pavel_kettlebell",
                            password="kettlebell",
                            email="pavel_kettle@kettlebell.org.com"))

        for i in range(1, 15):
            db_session.add(BodyWeightRecord(weight=random.randrange(900, 950) / 10.0,
                                            date=f"2023-02-{str(i).zfill(2)}",
                                            user_id=1))

            db_session.add(BodyWeightRecord(weight=random.randrange(700, 730) / 10.0,
                                            date=f"2023-02-{str(i).zfill(2)}",
                                            user_id=2))

            db_session.add(BodyWeightRecord(weight=random.randrange(820, 910) / 10.0,
                                            date=f"2023-02-{str(i).zfill(2)}",
                                            user_id=3))

            db_session.add(BodyWeightRecord(weight=random.randrange(790, 810) / 10.0,
                                            date=f"2023-02-{str(i).zfill(2)}",
                                            user_id=4))

        db_session.add(BlogPost(date=datetime.datetime.strptime("2024-02-01", "%Y-%m-%d"),
                                title="Welcome to the Fitness Tracker App!",
                                body="Hello guys! This is the first post here.\nWe will keep on working on the page "
                                     "and provide you the best user experience possible, for now let us wait a bit.",
                                user_id=1))

        db_session.add(BlogPost(date=datetime.datetime.strptime("2024-02-03", "%Y-%m-%d"),
                                title="Kettlebells for the win!",
                                body="Comrade! Forget those stupid barbells and other stuff.\n "
                                     "Just grab a pair of dumbbells and get ready to some pumping iron!",
                                user_id=4))
        db_session.commit()
