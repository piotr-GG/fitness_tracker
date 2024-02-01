from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from .dbc.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=False)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}, {self.email!r}>'


class BodyWeightRecord(Base):
    __tablename__ = "bw_records"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow, unique=True)
    weight = Column(Float)

    def __init__(self, weight=None, date=None):
        self.weight = weight
        self.date = datetime.strptime(date, "%Y-%m-%d").date()

    def __repr__(self):
        return f'<BW Record {self.id!r},{self.date!r},{self.weight!r}>'

    @classmethod
    def validate_bw_record(cls, bw_record):
        return True

    @staticmethod
    def create_bw_record(date, weight):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise Exception("Wrong value for date provided!")

        if date > datetime.utcnow().date():
            raise Exception("Date provided cannot be set in future!")

        try:
            weight = float(weight)
        except ValueError:
            raise Exception("Please provide valid value for body weight!")

        if not (0 <= weight <= 200):
            raise Exception("Body weight value shall be between 0 and 200 kgs!")

        return BodyWeightRecord(weight=weight, date=date)