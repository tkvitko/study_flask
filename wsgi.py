from werkzeug.security import generate_password_hash

from blog.app import create_app, db

app = create_app()


@app.cli.command("init-db", help="create all db")
def init_db():
    db.create_all()


@app.cli.command("create-users", help="create users")
def create_users():
    from blog.models import User
    db.session.add(
        User(username="tkvitko1", email="tkvitko@gmail.com", password=generate_password_hash("123456"), is_staff=True))
    db.session.add(
        User(username="tkvitko2", email="tkvitko@ab-technology.ru", password=generate_password_hash("qwerty"),
             is_staff=True))
    db.session.commit()


@app.cli.command("create-articles", help="create articles")
def create_articles():
    from blog.models import Article
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

    db.session.add(Article(title='Time for time', text=text, author_id=1))
    db.session.add(Article(title='Time for relax', text=text, author_id=2))
    db.session.add(Article(title='Cry In floor', text=text, author_id=1))
    db.session.add(Article(title='Crying floor', text=text, author_id=2))
    db.session.commit()


@app.cli.command("create-tags", help="create tags")
def create_tags():
    from blog.models import Tag
    for tag_name in ('tag1', 'tag2', 'tag3', 'tag4'):
        db.session.add(Tag(name=tag_name))
    db.session.commit()
