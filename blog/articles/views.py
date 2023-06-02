import requests

from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from flask_login import login_required

from blog.users.views import get_user_name

article = Blueprint("article", __name__, url_prefix="/articles", static_folder="../static")


@article.route("/")
@login_required
def article_list():
    from ..models import Article
    articles = Article.query.all()

    articles_count = requests.get('http://127.0.0.1/api/articles/event_get_count').text

    return render_template(
        "articles/list.html",
        articles=articles,
        articles_count=articles_count
    )


@article.route("/<int:pk>")
@login_required
def get_article(pk: int):

    from ..models import Article
    # article = Article.query.filter_by(id=pk).one_or_none()
    article = Article.query.filter_by(id=pk).options(joinedload(Article.tags)).one_or_none()
    if article is None:
        raise NotFound("Article id:{}, not found".format(pk))
    return render_template(
        "articles/details.html",
        article=article
    )
