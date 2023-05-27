from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from blog.admin.views import CustomAdminIndexView
from flask_admin import Admin

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(
    index_view=CustomAdminIndexView(),
    name='Blog Admin Panel',
    template_mode='bootstrap4',
)
