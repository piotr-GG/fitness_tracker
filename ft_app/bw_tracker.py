import json

from bokeh.models import ColumnDataSource, HoverTool
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)
from werkzeug.exceptions import abort

from ft_app import DBC
from ft_app.auth import login_required
from ft_app.forms import BodyWeightRecordForm
from ft_app.dbc.queries import get_bw_records_by_id, get_bw_record_by_id
from ft_app.models import BodyWeightRecord
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.io import curdoc
from bokeh.themes import Theme

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

            db_session = DBC.get_db_session()
            db_session.add(bw_record)
            db_session.commit()
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


@bp.route('/update/<int:bw_id>', methods=["GET", "POST"])
@login_required
def update(bw_id):
    form = BodyWeightRecordForm(request.form)
    bw_record_to_be_updated = get_bw_record_by_id(bw_id)

    if request.method == "POST":
        if form.validate():
            weight = request.form["weight"]
            bw_record_to_be_updated.weight = weight
            db_session = DBC.get_db_session()
            db_session.commit()
            return redirect(url_for("bw_tracker.index"))
        else:
            msg = form.print_error_message()
            flash(r"There were errors during updating. Please correct them.")
            for m in msg:
                flash(m)

    form.date.render_kw = {'disabled': 'disabled'}
    form.date.data = bw_record_to_be_updated.date
    form.weight.data = bw_record_to_be_updated.weight
    bw_records = get_bw_records_by_id(g.user.id)
    return render_template('bw_tracker/update.html',
                           records=bw_records,
                           form=form,
                           given_id=bw_id)


@bp.route('/delete/<int:bw_id>', methods=["GET", "POST"])
@login_required
def delete(bw_id):
    bw_record = get_bw_record_by_id(bw_id)
    if bw_record.user.id != g.user.id:
        abort(403, "Operation is forbidden. Reason: Attempting to delete record that does not belong to current user.")

    db_session = DBC.get_db_session()
    db_session.delete(bw_record)
    db_session.commit()
    flash("Bodyweight record has been successfully deleted!")
    return redirect(url_for("bw_tracker.index"))


def make_plot(x, y):
    p = figure(title="Body weight plot", sizing_mode="scale_both", width=800, height=400, x_axis_type="datetime")
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Body weight [kg]"
    source = ColumnDataSource(data=dict(date=x, weight=y))

    p.add_tools(
        HoverTool(
            tooltips=[
                ("Date", "@date{%F}"),
                ("Weight", "@weight{0.00}")
            ],
            formatters={
                '@date': 'datetime',
            },
            mode='vline'
        )
    )
    p.line(source=source, x="date", y="weight")
    p.scatter(source=source, x="date", y="weight")
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
