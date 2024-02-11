from flask import Blueprint, render_template

bp = Blueprint("training_planner", __name__, url_prefix="/tp")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("training_planner/index.html")
