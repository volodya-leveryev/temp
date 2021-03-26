from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_restful import Api

from fiit1.models import db, Author, Book


class BookAdmin(ModelView):
    column_labels = {
        'title': 'Название',
        'author2': 'Автор',
    }


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG')
    db.init_app(app)
    Migrate(app, db, render_as_batch=True)

    admin = Admin(app)
    admin.add_view(BookAdmin(Book, db.session))
    admin.add_view(ModelView(Author, db.session))

    from fiit1 import views
    api = Api(app)
    api.add_resource(views.BookList, '/')
    api.add_resource(views.Book, '/<int:book_id>/')

    return app
