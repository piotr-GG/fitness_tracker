from flask import Blueprint, render_template

from ft_app.auth import login_required

bp = Blueprint("training_planner", __name__, url_prefix="/tp")


@login_required
@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("training_planner/index.html",
                           training_plan=None)
