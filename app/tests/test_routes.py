import pytest
from datetime import datetime
from app import create_app, db
from app.models import Post


@pytest.fixture
def app():
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True
    })
    
    with app.app_context():
        db.create_all()
        yield app
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
        return post


def test_get_posts_empty(client):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert response.json == []


def test_create_post(client):
    data = {
        'title': 'New Post',
        'content': 'Post content'
    }
    response = client.post('/api/posts', json=data)
    assert response.status_code == 201
    assert response.json['title'] == 'New Post'
    assert response.json['content'] == 'Post content'
    assert 'id' in response.json
    assert 'created_at' in response.json


def test_create_post_validation_error(client):
    data = {
        'title': '',
        'content': 'Post content'
    }
    response = client.post('/api/posts', json=data)
    assert response.status_code == 400


def test_get_post(client, sample_post):
    response = client.get(f'/api/posts/{sample_post.id}')
    assert response.status_code == 200
    assert response.json['id'] == sample_post.id
    assert response.json['title'] == 'Test Post'
    assert response.json['content'] == 'Test Content'


def test_get_post_not_found(client):
    response = client.get('/api/posts/999')
    assert response.status_code == 404


def test_get_posts(client, sample_post):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id'] == sample_post.id


def test_update_post(client, sample_post):
    data = {
        'title': 'Updated Post',
        'content': 'Updated Content'
    }
    response = client.put(f'/api/posts/{sample_post.id}', json=data)
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Post'
    assert response.json['content'] == 'Updated Content'


def test_update_post_partial(client, sample_post):
    data = {
        'title': 'Updated Title Only'
    }
    response = client.put(f'/api/posts/{sample_post.id}', json=data)
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title Only'
    assert response.json['content'] == 'Test Content'


def test_update_post_not_found(client):
    data = {
        'title': 'Updated Post',
        'content': 'Updated Content'
    }
    response = client.put('/api/posts/999', json=data)
    assert response.status_code == 404


def test_update_post_validation_error(client, sample_post):
    data = {
        'title': '',
        'content': 'Updated Content'
    }
    response = client.put(f'/api/posts/{sample_post.id}', json=data)
    assert response.status_code == 400


def test_delete_post(client, sample_post):
    response = client.delete(f'/api/posts/{sample_post.id}')
    assert response.status_code == 200
    
    get_response = client.get(f'/api/posts/{sample_post.id}')
    assert get_response.status_code == 404


def test_delete_post_not_found(client):
    response = client.delete('/api/posts/999')
    assert response.status_code == 404

