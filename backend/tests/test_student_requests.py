import pytest
from tests.test_teachers import auth_header  # исправленный импорт

def test_student_request_flow(client):
    s = client.post(
        '/api/students',
        json={'full_name': 'Student', 'email': 's@mail.com'},
        headers=auth_header()
    ).json['id']

    t = client.post(
        '/api/teachers',
        json={'full_name': 'T', 'experience': 2, 'specialty': 'Biology', 'department': 'Sci'},
        headers=auth_header()
    ).json['id']
    c = client.post(
        '/api/courses',
        json={'title': 'Bio', 'teacher_id': t, 'student_limit': 1},
        headers=auth_header()
    ).json['id']

    r = client.post(
        '/api/requests',
        json={'student_id': s, 'course_id': c, 'description': 'Please'},
        headers=auth_header()
    )
    assert r.status_code == 201
    rid = r.json['id']

    u = client.put(f'/api/requests/{rid}', json={'status': 'approved'}, headers=auth_header())
    assert u.status_code == 200
    assert client.get(f'/api/requests/{rid}', headers=auth_header()).json['status'] == 'approved'