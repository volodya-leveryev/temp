from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from fiit1.models import db, Author, Book
from fiit1.views import login, BookList, BookResource, static_file


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
    JWTManager(app)

    app.add_url_rule('/', view_func=static_file)
    app.add_url_rule('/<path:filename>', view_func=static_file)
    app.add_url_rule('/login/', view_func=login, methods=['POST'])

    admin = Admin(app)
    admin.add_view(BookAdmin(Book, db.session))
    admin.add_view(ModelView(Author, db.session))

    api = Api(app)
    api.add_resource(BookList, '/book/')
    api.add_resource(BookResource, '/book/<int:book_id>/')

    return app
