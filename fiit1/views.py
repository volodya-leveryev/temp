from flask import jsonify, request

from fiit1 import db
from fiit1.models import Book


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
