import sys, os
import pytest

# Подключаем папку backend для импорта app
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(here, '..')))

from app import create_app
from app.models import db as _db

@pytest.fixture(scope='session')
def app():
    # Создаём приложение и настраиваем тестовую БД
    app = create_app()
    app.config['TESTING'] = True
    # Используем файл SQLite для тестов (in-memory на Windows иногда проблемен)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()