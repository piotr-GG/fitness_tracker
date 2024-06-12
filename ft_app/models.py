from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from ft_app.dbc.database import Base
from ft_app.forms import RegistrationForm


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=False)
    email = Column(String(120), unique=True)
    is_moderator = Column(Boolean(), default=False)

    blog_posts = relationship("BlogPost", back_populates="user")
    bw_records = relationship("BodyWeightRecord", back_populates="user")
    training_plans = relationship("TrainingPlan", back_populates="user")

    def __init__(self, username, password, email, is_moderator=False):
        form = RegistrationForm(username=username, email=email, password=password, confirm_pass=password)
        if form.validate():
            self.username = username
            self.password = generate_password_hash(password)
            self.email = email
            self.is_moderator = is_moderator
        else:
            res = form.print_error_message()
            raise ValueError("Values provided for User object are not valid. Please check errors below:\n" +
                             "\n".join(res))

    def __repr__(self):
        return f'<User {self.username!r}, {self.email!r}, is_moderator: {self.is_moderator!r}>'


class BodyWeightRecord(Base):
    __tablename__ = "bw_records"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float)
    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id"))

    user = relationship("User", back_populates="bw_records")

    def __init__(self, weight, date, user_id):
        self.weight = weight
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.user_id = user_id

    def __repr__(self):
        return f'<BW Record {self.id!r},{self.date!r},{self.weight!r}>'


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    last_edited = Column(DateTime, default=None, nullable=True)
    title = Column(String(200))
    body = Column(Text)
    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id"))

    user = relationship("User", back_populates="blog_posts")

    def __init__(self, date, title, body, user_id):
        self.date = date
        self.title = title
        self.body = body
        self.user_id = user_id


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    image_path = Column(String(200), default=None, nullable=True)

    exercise_records = relationship("ExerciseRecord", back_populates="exercise")

    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.image_path = image_path


class TrainingPlan(Base):
    __tablename__ = "training_plans"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id"), nullable=False)

    units = relationship("TrainingPlanUnit", back_populates="plan", cascade="all, delete-orphan")
    user = relationship("User", back_populates="training_plans")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f'<Training Plan {self.name!r}>'


class TrainingPlanUnit(Base):
    __tablename__ = 'training_plan_units'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    plan_id = Column(Integer, ForeignKey(f"{TrainingPlan.__tablename__}.id"))
    plan = relationship("TrainingPlan", back_populates="units")
    exercise_records = relationship("ExerciseRecord", back_populates="training_plan_unit")

    def __init__(self, name, date, plan_id):
        self.name = name
        self.date = date
        self.plan_id = plan_id

    def __repr__(self):
        return f'<Training Plan Unit {self.name!r}>'


class ExerciseRecord(Base):
    __tablename__ = "exercise_records"
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey(f"{Exercise.__tablename__}.id"))
    sets = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    training_plan_unit_id = Column(Integer, ForeignKey(f"{TrainingPlanUnit.__tablename__}.id"), nullable=False)

    exercise = relationship("Exercise", back_populates="exercise_records")
    training_plan_unit = relationship("TrainingPlanUnit", back_populates="exercise_records")

    def __init__(self, exercise_id, sets, repetitions, training_plan_unit_id):
        self.exercise_id = exercise_id
        self.sets = sets
        self.repetitions = repetitions
        self.training_plan_unit_id = training_plan_unit_id

    def __repr__(self):
        return f'<Exercise Record {self.exercise_id!r},{self.sets!r},{self.repetitions!r},{self.training_plan_unit_id!r}>'
