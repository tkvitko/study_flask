from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from flask_login import login_required

from blog.users.views import get_user_name

article = Blueprint("article", __name__, url_prefix="/articles", static_folder="../static")


@article.route("/")
@login_required
def article_list():
    from ..models import Article
    articles = Article.query.all()
    return render_template(
        "articles/list.html",
        articles=articles
    )


@article.route("/<int:pk>")
@login_required
def get_article(pk: int):

    from ..models import Article
    article = Article.query.filter_by(id=pk).one_or_none()
    if article is None:
        raise NotFound("Article id:{}, not found".format(pk))
    return render_template(
        "articles/details.html",
        article=article
    )
