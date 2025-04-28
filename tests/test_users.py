import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.db import User

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

def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_user(client):
    # Create a user
    hashed_password = generate_password_hash('password123')
    user = User(email='test@example.com', name='Test User', password_hash=hashed_password)
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully'

    # Get the user
    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'
    assert response.json['email'] == 'test@example.com'

    # Update the user
    response = client.patch('/api/users/1', json={
        'name': 'Updated Name',
        'email': 'updated@example.com'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User updated successfully'