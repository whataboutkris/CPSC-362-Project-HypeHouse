import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_listing(client):
    response = client.post('/api/listings', json={
        'title': 'Test Listing',
        'name': 'Test Host',
        'description': 'A test description',
        'photos': ['photo1.jpg', 'photo2.jpg'],
        'price': 100.0,
        'host_id': 1
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Listing created successfully'

def test_get_listings(client):
    response = client.get('/api/listings')
    assert response.status_code == 200
    assert isinstance(response.json, list)