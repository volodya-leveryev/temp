from flask import request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from fiit1 import db, models
from fiit1.models import User

parser = reqparse.RequestParser()
parser.add_argument('author')
parser.add_argument('title')


def static_file(filename='index.html'):
    return send_from_directory('static', filename)


def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({'success': False}), 401
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return jsonify({'success': False}), 401
    return jsonify({
        'success': True,
        'token': create_access_token(identity=username)
    }), 200


class BookList(Resource):
    @jwt_required()
    def get(self):
        return [{'title': b.title, 'author': b.author2_id} for b in models.Book.query.all()]

    def post(self):
        o = parser.parse_args()
        b = models.Book(title=o['title'])
        b.author2 = models.Author.query.get(o['author'])
        db.session.add(b)
        db.session.commit()
        return {'success': 1}


class BookResource(Resource):
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
