from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

auth = HTTPBasicAuth()

# Хранилище пользователей и ролей
users = {
    'admin': generate_password_hash('Sirius2025'),
    'user': generate_password_hash('userpass')
}
roles = {
    'admin': 'admin',
    'user': 'user'
}

@auth.verify_password
def verify(username, password):
    # В режиме тестирования (TestingConfig.TESTING = True)
    # любой запрос проходит как от 'admin'
    if current_app and current_app.config.get('TESTING'):
        return 'admin'

    # Обычная проверка имени и пароля
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    # Возвращаем список ролей для пользователя
    return [roles.get(user, 'user')]
