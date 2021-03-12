from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from database import db_session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    author = db.Column(db.String(100), unique=False)

    def __init__(self, title=None, author=None):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Book %r>' % self.title


def init_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:book_id>/', methods=['GET', 'PUT'])
def books(book_id=None):
    if request.method == 'POST':
        o = request.get_json()
        b = Book(o['title'], o['author'])
        db.session.add(b)
        db.session.commit()
        return jsonify(success=1)
    elif request.method == 'PUT':
        o = request.get_json()
        b = Book.query.get(book_id)
        b.title = o.get('title')
        b.author = o.get('author')
        db.session.add(b)
        db.session.commit()
        return jsonify(success=1)
    else:
        if book_id is not None and 0 < book_id:
            b = Book.query.filter(Book.id == book_id).first()
            if b:
                return jsonify({'title': b.title, 'author': b.author})
            else:
                return jsonify(success=0)
        else:
            b = [{'title': b.title, 'author': b.author} for b in Book.query.all()]
            return jsonify(b)


if __name__ == '__main__':
    app.run()
