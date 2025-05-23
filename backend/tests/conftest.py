import pytest
from app import create_app, db
from app.auth import auth

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers():
    return {}

@pytest.fixture(autouse=True)
def disable_auth(monkeypatch):
    monkeypatch.setattr(auth, 'login_required', lambda *args, **kwargs: (lambda f: f))
    yield
