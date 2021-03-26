import pytest

from fiit1 import create_app, db, models


LAST_NAME = 'Пушкин'
FIRST_NAME = 'Александр'
AUTHOR_ID = 1
TITLE = 'Евгений Онегин'


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            a = models.Author(last_name=LAST_NAME, first_name=FIRST_NAME)
            db.session.add(a)
            b = models.Book(title=TITLE)
            b.author2 = a
            db.session.add(b)
            db.session.commit()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_get_all(client):
    r = client.get('/')
    assert isinstance(r.json, list)
    assert len(r.json) == 1
    assert r.json[0].get('author') == AUTHOR_ID
    assert r.json[0].get('title') == TITLE


def test_get_first(client):
    r = client.get('/1/')
    assert isinstance(r.json, dict)
    assert r.json.get('author') == AUTHOR_ID
    assert r.json.get('title') == TITLE


def test_absent_book(client):
    r = client.get('/100500/')
    assert isinstance(r.json, dict)
    assert len(r.json) == 1
    assert r.json.get('success') == 0


def test_post_new_book(client):
    title2 = 'Герой нашего времени'
    r = client.post('/', json={
        'author': AUTHOR_ID,
        'title': title2,
    })
    assert isinstance(r.json, dict)
    assert len(r.json) == 1
    assert r.json.get('success') == 1

    r = client.get('/')
    assert isinstance(r.json, list)
    assert len(r.json) == 2
    assert AUTHOR_ID == r.json[1].get('author')
    assert title2 == r.json[1].get('title')


def test_update_existing_book(client):
    title2 = 'Герой нашего времени'
    res = client.put('/1/', json={
        'author': AUTHOR_ID,
        'title': title2,
    }).get_json()
    assert isinstance(res, dict)
    assert len(res) == 1
    assert res.get('success') == 1

    res = client.get('/1/').get_json()
    assert isinstance(res, dict)
    assert len(res) == 2
    assert AUTHOR_ID == res.get('author')
    assert title2 == res.get('title')

def test_delete_book(client):
    res = client.delete('/1/').get_json()
    assert isinstance(res, dict)
    assert len(res) == 1
    assert res.get('success') == 1

    res = client.get('/').get_json()
    assert isinstance(res, list)
    assert len(res) == 0
