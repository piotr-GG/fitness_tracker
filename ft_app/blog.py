from datetime import datetime

from flask import Blueprint, redirect, render_template, request, flash, session, url_for

from ft_app.forms import BlogPostCreateForm
from ft_app.models.dbc.database import db_session
from ft_app.models.dbc.queries import get_all_posts
from ft_app.models.models import BlogPost

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route('/', methods=["POST", "GET"])
def index():
    posts = get_all_posts()
    return render_template("blog/index.html", posts=posts)


@bp.route('/create', methods=["POST", "GET"])
def create():
    form = BlogPostCreateForm(request.form)
    if request.method == "POST":
        if form.validate():
            new_blog_post = BlogPost(
                date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
                title=request.form["title"],
                body=request.form["body"],
                user_id=session.get('user_id')
            )
            db_session.add(new_blog_post)
            db_session.commit()
            flash("New blog post has been successfully created!")
            return redirect(url_for('blog.index'))
        else:
            msg = form.print_error_message()
            flash(r"There were errors during registration. Please correct them.")
            for m in msg:
                flash(m)
    return render_template("blog/create.html", form=form)
