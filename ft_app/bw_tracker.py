import json

from bokeh.sampledata.iris import flowers
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)

from ft_app.models.dbc.queries import get_bw_records_by_id
from ft_app.models.models import BodyWeightRecord
from ft_app.models.dbc.database import db_session
from bokeh.plotting import figure
from bokeh.embed import components, json_item

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
            plot = figure()
            plot.circle([1, 2], [3, 4])
            script, div = components(plot)
            return render_template('bw_tracker/index.html',
                                   records=bw_records)
        else:
            flash("You need to be logged in in order to use BodyWeightTracker")
            return redirect(url_for("auth.login"))


colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]


def make_plot(x, y):
    p = figure(title="Iris Morphology", sizing_mode="fixed", width=400, height=400)
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p


@bp.route('/plot')
def plot():
    p = make_plot('petal_width', 'petal_length')
    return json.dumps(json_item(p, "myplot"))
