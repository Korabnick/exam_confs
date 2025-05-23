def test_course_crud(client, admin_headers):
    teacher = client.post('/api/teachers', json={
        'full_name': 'Course Teacher',
        'experience': 10,
        'specialty': 'Информатика',
        'department': 'ИТ'
    }, headers=admin_headers).get_json()
    t_id = teacher['id']

    create = client.post('/api/courses', json={
        'title': 'Python 101',
        'teacher_id': t_id,
        'student_limit': 30
    }, headers=admin_headers)
    assert create.status_code == 201
    c_id = create.get_json()['id']

    get = client.get(f'/api/courses/{c_id}', headers=admin_headers)
    assert get.status_code == 200

    patch = client.patch(f'/api/courses/{c_id}', json={
        'student_limit': 35
    }, headers=admin_headers)
    assert patch.status_code == 200

    delete = client.delete(f'/api/courses/{c_id}', headers=admin_headers)
    assert delete.status_code == 200
