from datetime import datetime

from sqlalchemy import Column  # , Integer, DateTime, Float
from ft_app.app import db


class BodyWeightRecord(db.Model):
    id = Column(db.Integer, primary_key=True)
    date = Column(db.DateTime, default=datetime.utcnow)

    # weight = Column(Float)

    def __repr__(self):
        return f'<BW Record {self.id}>'
