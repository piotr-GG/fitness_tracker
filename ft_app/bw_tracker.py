import json

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)

from ft_app.auth import login_required
from ft_app.forms import BodyWeightRecordForm
from ft_app.dbc.queries import get_bw_records_by_id
from ft_app.models import BodyWeightRecord
from bokeh.plotting import figure
from bokeh.embed import json_item

bp = Blueprint("bw_tracker", __name__, url_prefix="/bw_tracker")


@login_required
@bp.route('/', methods=['POST', 'GET'])
def index():
    form = BodyWeightRecordForm(request.form)
    if request.method == "POST":
        if form.validate():
            bw_record = BodyWeightRecord(weight=request.form["weight"],
                                         date=request.form["date"],
                                         user_id=g.user.id)

            for record in g.user.bw_records:
                if bw_record.date == record.date.date():
                    flash("There is already body weight record for given date!")
                    return redirect('/bw_tracker')

            g.db_session.add(bw_record)
            g.db_session.commit()
            flash("Body weight record has been properly added!")
            return redirect('/bw_tracker')
        else:
            msg = form.print_error_message()
            flash(r"There were errors during adding body weight record. Please correct them.")
            for m in msg:
                flash(m)
            return redirect('/bw_tracker')
    else:
        if g.user:
            bw_records = get_bw_records_by_id(g.user.id)
            return render_template('bw_tracker/index.html',
                                   records=bw_records,
                                   form=form)
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
