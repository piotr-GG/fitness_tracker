from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from .dbc.database import Base
from ..forms import RegistrationForm


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=False)
    email = Column(String(120), unique=True)
    is_moderator = Column(Boolean(), default=False)

    blog_posts = relationship("BlogPost", back_populates="user")
    bw_records = relationship("BodyWeightRecord", back_populates="user")

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
    date = Column(DateTime, default=datetime.utcnow, unique=True)
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
