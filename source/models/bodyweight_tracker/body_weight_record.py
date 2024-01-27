from datetime import datetime
from app import db


class BodyWeightRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float)

    def __repr__(self):
        return f'<BW Record {self.id}>'

