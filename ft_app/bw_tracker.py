from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from ft_app.models.models import BodyWeightRecord

bp = Blueprint("bw_tracker", __name__)


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        return "POSTING!"
    else:
        bw_records = BodyWeightRecord.query.all()
        return render_template('index.html', records=bw_records)
