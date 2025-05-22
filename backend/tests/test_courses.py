import pytest
from tests.test_teachers import auth_header  # импорт из sibling-модуля в backend/tests

def test_course_workflow(client):
    # создаём учителя
    teacher = client.post(
        '/api/teachers',
        json={'full_name': 'C T', 'experience': 3, 'specialty': 'Math', 'department': 'Fac'},
        headers=auth_header()
    ).json['id']

    # GET empty courses
    r0 = client.get('/api/courses', headers=auth_header())
    assert r0.status_code == 200
    assert r0.json == []

    # Create course
    payload = {'title': 'Algebra', 'teacher_id': teacher, 'student_limit': 10}
    r1 = client.post('/api/courses', json=payload, headers=auth_header())
    assert r1.status_code == 201
    cid = r1.json['id']

    # Get by ID
    g = client.get(f'/api/courses/{cid}', headers=auth_header())
    assert g.status_code == 200
    assert g.json['teacher_id'] == teacher