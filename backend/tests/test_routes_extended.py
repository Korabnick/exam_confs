import pytest
from flask import url_for

# TEST: отсутствие обязательных полей → 400
@pytest.mark.parametrize("endpoint,payload,missing", [
    ("/api/teachers", {'experience': 3, 'specialty': 'X', 'department': 'Y'}, 'full_name'),
    ("/api/courses", {'title': 'C1', 'student_limit': 5}, 'teacher_id'),
    ("/api/students", {'email': 'a@b.c'}, 'full_name'),
    ("/api/requests", {'student_id': 1}, 'course_id'),
])
def test_create_missing_field(client, admin_headers, endpoint, payload, missing):
    resp = client.post(endpoint, json=payload, headers=admin_headers)
    assert resp.status_code == 400

# TEST: GET для несуществующего объекта → 404
@pytest.mark.parametrize("endpoint", [
    "/api/teachers/999",
    "/api/courses/999",
    "/api/students/999",
    "/api/requests/999",
])
def test_get_not_found(client, admin_headers, endpoint):
    resp = client.get(endpoint, headers=admin_headers)
    assert resp.status_code == 404

# TEST: запрещённый метод на эндпоинте (например, DELETE без id на коллекции) → 405
def test_invalid_method(client, admin_headers):
    resp = client.delete("/api/teachers", headers=admin_headers)
    assert resp.status_code == 405
