from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound


user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")
USERS = {
    1: {"name": "Taras", "email": "tkvitko@gmail.com"},
    2: {"name": "Marina", "email": "tkvitko1@gmail.com"},
    3: {"name": "Diana", "email": "tkvitko2@gmail.com"},
    5: {"name": "Victoria", "email": "tkvitko3@gmail.com"}
}


@user.route("/")
def user_list():
    users = USERS
    return render_template(
        "users/list.html",
        users=users
    )


@user.route("/<int:pk>")
def profile(pk: int):
    if pk not in USERS.keys():
        raise NotFound(f"User id: {pk}, not found")
    return render_template(
        "users/details.html",
        user=USERS[pk]
    )


def get_user_name(pk: int):
    if pk in USERS:
        user_name = USERS[pk]["name"]
    else:
        raise NotFound("User id:{}, not found".format(pk))
    return user_name
