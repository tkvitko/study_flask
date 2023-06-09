import flask_bcrypt
from flask_login import UserMixin
from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship

from .app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.String(255), nullable=False, default="", server_default="")
    _password = db.Column(db.LargeBinary, nullable=True)
    articles = relationship("Article", back_populates="author")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

    def __str__(self):
        return f'{self.user.email} ({self.user.id})'


article_tag_association_table = db.Table(
    "article_tag_association",
    db.metadata,
    db.Column("article_id", db.Integer, ForeignKey("articles.id"), nullable=False),
    db.Column("tag_id", db.Integer, ForeignKey("tags.id"), nullable=False),
)


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    text = db.Column(db.String(1024))
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # author: Mapped["User"] = relationship()
    author_id = db.Column(db.Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="articles")
    tags = relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )

    def __str__(self):
        return self.title


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, default="", server_default="")
    articles = relationship(
        "Article",
        secondary=article_tag_association_table,
        back_populates="tags",
    )

    def __str__(self):
        return self.name
