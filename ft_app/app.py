from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


def get_db():
    return db


# class BodyWeightRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     weight = db.Column(db.Float)
#
#     def __repr__(self):
#         return f'<BW Record {self.id}>'


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db = SQLAlchemy(app)

    @app.route('/')
    def index():
        from models.bodyweight_tracker.body_weight_record import BodyWeightRecord
        bw_records = BodyWeightRecord.query.all()
        return render_template('index.html', records=bw_records)

    app.run(debug=True)
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as exc:
            print("Got the following expection when attempting to db.create_all()" + str(exc))



