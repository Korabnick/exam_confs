import base64
import pytest

def auth_header(username='admin', password='Sirius2025'):
    cred = f"{username}:{password}".encode()
    token = base64.b64encode(cred).decode()
    return {'Authorization': f'Basic {token}'}

def test_get_teachers_empty(client):
    resp = client.get('/api/teachers', headers=auth_header())
    assert resp.status_code == 200
    assert resp.json == []

@pytest.mark.parametrize('payload', [
    {'full_name': 'Test Teacher', 'experience': 5, 'specialty': 'Physics', 'department': 'Science'}
])
def test_create_and_get_teacher(client, payload):
    r = client.post('/api/teachers', json=payload, headers=auth_header())
    assert r.status_code == 201
    tid = r.json['id']
    g = client.get(f'/api/teachers/{tid}', headers=auth_header())
    assert g.status_code == 200
    data = g.json
    assert data['full_name'] == payload['full_name']
    assert data['experience'] == payload['experience']