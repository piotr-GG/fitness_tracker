from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from ft_app.models.models import BodyWeightRecord
from ft_app.models.dbc.database import db_session

bp = Blueprint("bw_tracker", __name__, url_prefix="/bw_tracker")


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        try:
            bw_record = BodyWeightRecord.create_bw_record(request.form["date"],
                                                          request.form["weight"])
        except Exception as e:
            flash(str(e))
            return redirect('/bw_tracker')

        added_info = f"""
            Date: {request.form["date"]},
            Weight: {request.form["weight"]}
        """
        print(added_info)
        db_session.add(bw_record)
        db_session.commit()
        return redirect('/bw_tracker')

    else:
        bw_records = BodyWeightRecord.query.all()
        return render_template('bw_tracker/index.html', records=bw_records)
