from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from users.views import get_user_name

article = Blueprint("article", __name__, url_prefix="/articles", static_folder="../static")

TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
ARTICLES = {
    1: {
        "title": "Time for time",
        "text": TEXT,
        "author": 2
    },
    2: {
        "title": "Time for relax",
        "text": TEXT,
        "author": 2
    },
    3: {
        "title": "Cry In floor",
        "text": TEXT,
        "author": 1
    },
    4: {
        "title": "Crying floor",
        "text": TEXT,
        "author": 3
    }
}


@article.route("/")
def article_list():
    return render_template(
        "articles/list.html",
        articles=ARTICLES
    )


@article.route("/<int:pk>")
def get_article(pk: int):
    if pk in ARTICLES:
        article_raw = ARTICLES[pk]
    else:
        raise NotFound("Article id:{}, not found".format(pk))
    title = article_raw["title"]
    text = article_raw["text"]
    author = get_user_name(article_raw["author"])
    return render_template(
        "articles/details.html",
        title=title,
        text=text,
        author=author
    )
