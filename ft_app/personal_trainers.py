from flask import Blueprint, render_template

bp = Blueprint("personal_trainers", __name__, url_prefix="/pts")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("personal_trainers/index.html")
