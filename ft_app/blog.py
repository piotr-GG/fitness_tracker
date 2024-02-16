from datetime import datetime

from flask import Blueprint, redirect, render_template, request, flash, session, url_for, g
from werkzeug.exceptions import abort

from ft_app import DBC
from ft_app.auth import login_required
from ft_app.forms import BlogPostCreateForm
from ft_app.dbc.queries import get_all_posts, get_post_by_id
from ft_app.models import BlogPost

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route('/', methods=["POST", "GET"])
def index():
    posts = get_all_posts()
    return render_template("blog/index.html", posts=posts)


@bp.route('/create', methods=["POST", "GET"])
@login_required
def create():
    form = BlogPostCreateForm(request.form)
    if not g.user.is_moderator:
        abort(403)

    if request.method == "POST":
        if form.validate():
            new_blog_post = BlogPost(
                date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
                title=request.form["title"],
                body=request.form["body"],
                user_id=session.get('user_id')
            )
            db_session = DBC.get_db_session()
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


@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    blog_post = get_post_by_id(post_id)
    form = BlogPostCreateForm(request.form)
    form.date.render_kw = {'disabled': 'disabled'}
    form.title.data = blog_post.title
    form.body.data = blog_post.body

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        blog_post.title = title
        blog_post.body = body
        blog_post.last_edited = datetime.strptime(str(datetime.utcnow().date()), "%Y-%m-%d").date()

        db_session = DBC.get_db_session()
        db_session.commit()
        return redirect(url_for('blog.index'))

    return render_template("blog/update.html", form=form)


@bp.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = get_post_by_id(post_id)
    db_session = DBC.get_db_session()
    db_session.delete(post)
    db_session.commit()
    flash("Your post has been successfully deleted!")
    return redirect(url_for("blog.index"))
