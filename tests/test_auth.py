import pytest
from app.models.user import User

def test_register(client, app):
    response = client.post('/register', data={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'Your account has been created' in response.data
    
    with app.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None

def test_login(client, test_user):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Dashboard' in response.data

def test_unauthorized_access(client):
    response = client.get('/dashboard', follow_redirects=True)
    # Flask-Login redirects to login with a message
    assert b'Please log in to access this page.' in response.data
