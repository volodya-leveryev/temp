from flask import Flask, jsonify, request

from database import db_session
from models import Book

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:book_id>')
def books(book_id=None):
    if request.method == 'POST':
        b = Book(request.form['title'], request.form['author'])
        db_session.add(b)
        db_session.commit()
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


@app.teardown_appcontext
def shutdown_session(_=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
