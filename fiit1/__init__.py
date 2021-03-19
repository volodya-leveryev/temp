from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api

from fiit1.models import db, Book


class BookAdmin(ModelView):
    column_labels = {
        'title': 'Название',
        'author': 'Автор',
    }


def init_db():
    db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    admin = Admin(app)
    admin.add_view(BookAdmin(Book, db.session))

    from fiit1 import views
    api = Api(app)
    api.add_resource(views.BookList, '/')
    api.add_resource(views.Book, '/<int:book_id>/')

    return app
