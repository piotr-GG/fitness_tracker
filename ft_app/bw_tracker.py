import json
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)

from ft_app.auth import login_required
from ft_app.models.dbc.queries import get_bw_records_by_id
from ft_app.models.models import BodyWeightRecord
from ft_app.models.dbc.database import db_session
from bokeh.plotting import figure
from bokeh.embed import json_item

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
        if g.user:
            bw_records = get_bw_records_by_id(g.user.id)
            return render_template('bw_tracker/index.html',
                                   records=bw_records)
        else:
            flash("You need to be logged in in order to use BodyWeightTracker")
            return redirect(url_for("auth.login"))


def make_plot(x, y):
    p = figure(title="Body weight plot", sizing_mode="fixed", width=800, height=400, x_axis_type="datetime")
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Body weight [kg]"
    p.line(x, y)
    p.scatter(x, y)
    return p


@login_required
@bp.route('/plot')
def plot():
    if g.user:
        data = get_bw_records_by_id(g.user.id)
        x, y = [], []
        for record in data:
            x.append(record.date)
            y.append(record.weight)
        p = make_plot(x, y)
        return json.dumps(json_item(p, "myplot"))
