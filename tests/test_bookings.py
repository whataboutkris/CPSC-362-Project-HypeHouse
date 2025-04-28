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

def test_confirm_booking(client):
    response = client.post('/api/confirm_booking', json={
        'listing_id': 1,
        'start_date': '2025-05-01',
        'end_date': '2025-05-10'
    })
    assert response.status_code == 302 # Redirect status code
    # assert response.json['message'] == 'Booking confirmed successfully'

def test_cancel_booking(client):
    response = client.delete('/api/bookings/1')
    assert response.status_code == 302
    #assert response.json['message'] == 'Booking cancelled successfully!'