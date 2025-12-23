import pytest

from app import create_app, db
from app.models import Post


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_post(app):
    with app.app_context():
        post = Post(title='Test Post', content='Test Content')
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        return post_id


def test_get_post(client, sample_post):
    response = client.get(f'/api/posts/{sample_post}')
    assert response.status_code == 200
    assert response.json['id'] == sample_post


def test_update_post(client, sample_post):
    data = {'title': 'Updated Post', 'content': 'Updated Content'}
    response = client.put(f'/api/posts/{sample_post}', json=data)
    assert response.status_code == 200


def test_delete_post(client, sample_post):
    response = client.delete(f'/api/posts/{sample_post}')
    assert response.status_code == 200
