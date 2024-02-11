from flask import Blueprint, render_template

bp = Blueprint("about", __name__, url_prefix="/about")


@bp.route('/')
def index():
    return render_template("about/index.html")
