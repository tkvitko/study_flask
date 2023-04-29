from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@user.route("/")
@login_required
def user_list():
    from ..models import User
    users = User.query.all()
    return render_template(
        "users/list.html",
        users=users
    )


def one_or_none():
    pass


@user.route("/<int:pk>")
@login_required
def profile(pk: int):
    from ..models import User, Article
    _user = User.query.filter_by(id=pk).one_or_none()
    articles = Article.query.join(User).filter(User.id == pk).all()
    if _user is None:
        raise NotFound("User id:{}, not found".format(pk))
    return render_template(
        "users/details.html",
        user=_user,
        articles=articles
    )


def get_user_name(pk: int):
    from ..models import User
    _user = User.query.filter_by(id=pk).one_or_none()
    if _user is None:
        raise NotFound("User id:{}, not found".format(pk))
    return _user.email
