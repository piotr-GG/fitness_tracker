import datetime
import os
from flask import Flask, render_template
from ft_app.dbc.database import DBC

db_session = DBC.db_session


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
    if not User.query.all():
        db_session.add(User(username="adrian", password="1234567", email="ceo@gmail.com", is_moderator=True))
        db_session.add(User(username="ganesh", password="ganesh", email="ganesh@gmail.com"))

        db_session.add(BodyWeightRecord(weight=90.5, date="2023-01-01", user_id=1))
        db_session.add(BodyWeightRecord(weight=91.2, date="2023-01-02", user_id=1))
        db_session.add(BodyWeightRecord(weight=92.5, date="2023-01-03", user_id=1))
        db_session.add(BodyWeightRecord(weight=95.5, date="2023-01-04", user_id=1))

        db_session.add(BodyWeightRecord(weight=68.5, date="2023-02-01", user_id=2))
        db_session.add(BodyWeightRecord(weight=71.2, date="2023-02-02", user_id=2))
        db_session.add(BodyWeightRecord(weight=65.5, date="2023-02-03", user_id=2))
        db_session.add(BodyWeightRecord(weight=67.5, date="2023-02-04", user_id=2))

        db_session.add(BlogPost(date=datetime.datetime.utcnow(),
                                title="yyyy, eee, yyy",
                                body="Poczekajcie, muszę pomyśleć!",
                                user_id=1))

        db_session.add(BlogPost(date=datetime.datetime.utcnow(),
                                title="Jestem największym koksem",
                                body="Jestem Szefem, ja jestem Szefem!",
                                user_id=1))
        db_session.commit()
