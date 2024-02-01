from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from ft_app.models.models import BodyWeightRecord
from ft_app.models.dbc.database import db_session

bp = Blueprint("bw_tracker", __name__)


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        bw_record = BodyWeightRecord(weight=request.form["weight"],
                                     date=request.form["date"])
        is_correctly_input = BodyWeightRecord.validate_bw_record(bw_record)
        if is_correctly_input:
            added_info = f"""
                Date: {request.form["date"]},
                Weight: {request.form["weight"]}
            """
            print(added_info)
            db_session.add(bw_record)
            db_session.commit()
            return redirect('/')
        else:
            return "Input is wrong. Please try again!"

    else:
        bw_records = BodyWeightRecord.query.all()
        return render_template('index.html', records=bw_records)
