from datetime import datetime

from flask_sqlalchemy.model import Model
from sqlalchemy import Column, Integer, DateTime, Float


class BodyWeightRecord(Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float)

    def __repr__(self):
        return f'<BW Record {self.id}>'
