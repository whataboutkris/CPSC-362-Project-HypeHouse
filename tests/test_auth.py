import pytest
from app import create_app, db
from werkzeug.security import generate_password_hash
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

def test_register(client):
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_login(client):
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