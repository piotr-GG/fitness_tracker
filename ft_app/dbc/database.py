from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

Base = declarative_base()


class DBC:
    _engine = None
    _db_session = None

    @staticmethod
    def create_engine():
        DBC._engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}", pool_size=25, max_overflow=100)

    @staticmethod
    def create_db_session():
        DBC._db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=DBC._engine))

    @staticmethod
    def init_db():
        # noinspection PyUnresolvedReferences
        import ft_app.models
        DBC.create_engine()
        DBC.create_db_session()
        Base.metadata.create_all(bind=DBC._engine)

    @staticmethod
    def get_db_session():
        return DBC._db_session
