from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from ft_app.models.models import *


def init_db():
    Base.metadata.create_all(bind=engine)
