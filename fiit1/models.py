from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    author = db.Column(db.String(100), unique=False)

    def __init__(self, title=None, author=None):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Book %r>' % self.title
