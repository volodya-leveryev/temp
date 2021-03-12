import pytest

from app import app, db, Book


AUTHOR = 'Александр Пушкин'
TITLE = 'Евгений Онегин'


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

    with app.test_client() as client:
        with app.app_context():
            b = Book(title=TITLE, author=AUTHOR)
            db.create_all()
            db.session.add(b)
            db.session.commit()
        yield client

    db.session.remove()
    db.drop_all()


def test_get_all(client):
    r = client.get('/')
    assert isinstance(r.json, list)
    assert len(r.json) == 1
    assert r.json[0].get('author') == AUTHOR
    assert r.json[0].get('title') == TITLE


def test_get_first(client):
    r = client.get('/1/')
    assert isinstance(r.json, dict)
    assert r.json.get('author') == AUTHOR
    assert r.json.get('title') == TITLE


def test_absent_book(client):
    r = client.get('/100500/')
    assert isinstance(r.json, dict)
    assert len(r.json) == 1
    assert r.json.get('success') == 0


def test_post_new_book(client):
    author2 = 'Михаил Лермонтов'
    title2 = 'Герой нашего времени'
    r = client.post('/', json={
        'author': author2,
        'title': title2,
    })
    assert isinstance(r.json, dict)
    assert len(r.json) == 1
    assert r.json.get('success') == 1

    r = client.get('/')
    assert isinstance(r.json, list)
    assert len(r.json) == 2
    assert author2 == r.json[1].get('author')
    assert title2 == r.json[1].get('title')


def test_update_existing_book(client):
    author2 = 'Михаил Лермонтов'
    title2 = 'Герой нашего времени'
    res = client.put('/1/', json={
        'author': author2,
        'title': title2,
    }).get_json()
    assert isinstance(res, dict)
    assert len(res) == 1
    assert res.get('success') == 1

    res = client.get('/1/').get_json()
    assert isinstance(res, dict)
    assert len(res) == 2
    assert author2 == res.get('author')
    assert title2 == res.get('title')
