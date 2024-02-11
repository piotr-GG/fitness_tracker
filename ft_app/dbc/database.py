from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

Base = declarative_base()


class DBC:
    engine = None
    db_session = None

    @staticmethod
    def create_engine():
        DBC.engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}")

    @staticmethod
    def create_db_session():
        DBC.db_session = scoped_session(sessionmaker(autocommit=False,
                                                     autoflush=False,
                                                     bind=DBC.engine))

    @staticmethod
    def init_db():
        from ft_app.models import User, BlogPost, BodyWeightRecord
        DBC.create_engine()
        DBC.create_db_session()
        Base.metadata.create_all(bind=DBC.engine)
