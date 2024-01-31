from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from ft_app.models.models import BodyWeightRecord

bp = Blueprint("bw_tracker", __name__)


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        added_info = f"""
            Date: {request.form["date"]},
            Weight: {request.form["weight"]}
        """
        return added_info
    else:
        bw_records = BodyWeightRecord.query.all()
        return render_template('index.html', records=bw_records)
