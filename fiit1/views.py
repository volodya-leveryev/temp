from flask_restful import Resource, reqparse

from fiit1 import db, models

parser = reqparse.RequestParser()
parser.add_argument('author')
parser.add_argument('title')


class BookList(Resource):
    def get(self):
        return [{'title': b.title, 'author': b.author2_id} for b in models.Book.query.all()]

    def post(self):
        o = parser.parse_args()
        b = models.Book(title=o['title'])
        b.author2 = models.Author.query.get(o['author'])
        db.session.add(b)
        db.session.commit()
        return {'success': 1}


class Book(Resource):
    def get(self, book_id):
        b = models.Book.query.get(book_id)
        if b is None:
            return {'success': 0}
        else:
            return {'title': b.title, 'author': b.author2_id}

    def put(self, book_id):
        o = parser.parse_args()
        b = models.Book.query.get(book_id)
        b.author = o['author']
        b.title = o['title']
        db.session.add(b)
        db.session.commit()
        return {'success': 1}

    def delete(self, book_id):
        b = models.Book.query.get(book_id)
        db.session.delete(b)
        db.session.commit()
        return {'success': 1}
