from sqlalchemy.exc import IntegrityError

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import logout_user, login_user, login_required, LoginManager, current_user
from blog.forms.user import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash
from werkzeug.exceptions import NotFound
from blog.models import User
from blog.forms.user import LoginForm
from blog.extension import db

auth = Blueprint("auth", __name__, url_prefix="/auth", static_folder="../static")

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


__all__ = [
    "login_manager",
    "auth",
]


@auth.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.main_page"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        if not user.validate_password(form.password.data):
            return render_template("auth/login.html", form=form, error="invalid username or password")
        login_user(user)
        return redirect(url_for("index.main_page"))
    return render_template("auth/login.html", form=form)


@auth.route("/logout", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.main_page"))


@auth.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        # non-admin users should not know about this feature
        raise NotFound


@auth.route("/secret")
@login_required
def secret_view():
    return "Super secret data"


@auth.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index.main_page"))
    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("index.main_page"))
            # return redirect("index.main_page")
    return render_template("auth/register.html", form=form, error=error)

# @auth.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template(
#             "auth/login.html"
#         )
#     from ..models import User
#
#     email = request.form.get("email")
#     password = request.form.get("password")
#     user = User.query.filter_by(email=email).first()
#
#     if not user or not check_password_hash(user.password, password):
#         flash("Check your login details")
#         return redirect(url_for(".login"))
#     login_user(user)
#     return redirect(url_for("user.profile", pk=user.id))
#
#
# @auth.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for(".login"))
