from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(metadata=metadata)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    author2 = db.relationship('Author', backref='books', lazy=True)
    author2_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __init__(self, title=None, author=None):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Book %r>' % self.title


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30))

    def __str__(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result
