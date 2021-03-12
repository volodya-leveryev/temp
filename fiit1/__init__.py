from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from fiit1 import views
    app.add_url_rule('/', 'book', views.books, methods=['GET', 'POST'])
    app.add_url_rule('/<int:book_id>/', 'book', views.books, methods=['GET', 'PUT'])

    return app
