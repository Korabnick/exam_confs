from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

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
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    return [roles.get(user, 'user')]