import datetime
import os
import random

from flask import Flask, render_template
from ft_app.dbc.database import DBC
from ft_app.models import Exercise, TrainingPlan, TrainingPlanUnit, ExerciseRecord


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
                                            date=f"2024-05-{str(i).zfill(2)}",
                                            user_id=1))

            db_session.add(BodyWeightRecord(weight=random.randrange(700, 730) / 10.0,
                                            date=f"2024-05-{str(i).zfill(2)}",
                                            user_id=2))

            db_session.add(BodyWeightRecord(weight=random.randrange(820, 910) / 10.0,
                                            date=f"2024-05-{str(i).zfill(2)}",
                                            user_id=3))

            db_session.add(BodyWeightRecord(weight=random.randrange(790, 810) / 10.0,
                                            date=f"2024-05-{str(i).zfill(2)}",
                                            user_id=4))

        db_session.add(BlogPost(date=datetime.datetime.strptime("2024-06-01", "%Y-%m-%d"),
                                title="Welcome to the Fitness Tracker App!",
                                body="Hello guys! This is the first post here.\nWe will keep on working on the page "
                                     "and provide you the best user experience possible, for now let us wait a bit.",
                                user_id=1))

        db_session.add(BlogPost(date=datetime.datetime.strptime("2024-06-03", "%Y-%m-%d"),
                                title="Kettlebells for the win!",
                                body="Comrade! Forget those stupid barbells and other stuff.\n "
                                     "Just grab a pair of dumbbells and get ready to some pumping iron!",
                                user_id=4))

        db_session.add(Exercise(name="Barbell Squat",
                                description="Squat is a compound exercise that primarily works the quads and glutes.",
                                image_path="barbell_squat.jpg"))

        db_session.add(Exercise(name="Deadlift",
                                description="King of all exercises, the might deadlift will make your whole body work "
                                            "as a one unit.",
                                image_path="deadlift.jpg"))

        db_session.add(Exercise(name="Bench Press",
                                description="The bench press is a compound exercise that primarily works the chest.",
                                image_path="bench_press.jpg"))

        db_session.add(Exercise(name="Bicep curl",
                                description="The curl primarily works the biceps and is a key to developing crazy "
                                            "biceps.",
                                image_path="bicep_curl.jpg"))

        db_session.add(Exercise(name="Tricep pressdown",
                                description="The tricep pressdown is an isolation exercise that primarily works the "
                                            "triceps.",
                                image_path="tricep_pressdown.jpg"))

        db_session.add(Exercise(name="Calf raise",
                                description="Calf raises are an isolation exercise that primarily works the "
                                            "calves.",
                                image_path="calf_raise.jpg"))

        db_session.add(Exercise(name="Plank",
                                description="Planks are an isometric exercise that works your entire "
                                            "core muscles.",
                                image_path="plank.jpg"))

        db_session.add(Exercise(name="Dumbbell press",
                                description="The dumbbell press is an exercise that  works the chest and"
                                            "shoulders.",
                                image_path="dumbbell_press.jpg"))

        db_session.add(Exercise(name="Overhead press",
                                description="Overhead press is an exercise that works the shoulders.",
                                image_path="overhead_press.jpg"))

        db_session.add(Exercise(name="Barbell row",
                                description="Excellent exercise for developing the back muscles.",
                                image_path="barbell_row.jpg"))

        db_session.add(Exercise(name="Dumbbell row",
                                description="Single-arm version of the row for developing the "
                                            "back muscles.",
                                image_path="dumbbell_row.jpg"))

        db_session.add(Exercise(name="Cable row",
                                description="Cable version of the row for developing the back "
                                            "muscles.",
                                image_path="cable_row.jpg"))

        db_session.add(Exercise(name="Dips",
                                description="Bodyweight exercise that primarily works the chest and "
                                            "triceps.",
                                image_path="dips.jpg"))

        db_session.add(Exercise(name="Pull-ups",
                                description="King of all bodyweight exercises that works your upper "
                                            "body.",
                                image_path="pull_ups.jpg"))

        db_session.add(Exercise(name="Push-ups",
                                description="Staple of any body weight training, it will work your "
                                            "chest and triceps, plus core!.",
                                image_path="push_ups.jpg"))

        db_session.add(Exercise(name="Chin-ups",
                                description="Version of pull-up that will work your bicep more that "
                                            "in pull-ups alone.",
                                image_path="chin_ups.jpg"))

        db_session.add(Exercise(name="Lunge",
                                description="Lunge will work your whole lower body with additional "
                                            "benefit of developing your core muscles as well.",
                                image_path="lunge.jpg"))

        test_tp = TrainingPlan(name="My training plan")
        db_session.add(test_tp)
        db_session.commit()

        test_tp_unit = TrainingPlanUnit(name="Monday",
                                        date=datetime.datetime.strptime("2024-06-03", "%Y-%m-%d"),
                                        plan_id=test_tp.id)
        db_session.add(test_tp_unit)
        db_session.commit()

        test_ex_r = ExerciseRecord(exercise_id=1,
                                   sets=3,
                                   repetitions=10,
                                   unit_id=test_tp_unit.id)
        db_session.add(test_ex_r)
        db_session.commit()
