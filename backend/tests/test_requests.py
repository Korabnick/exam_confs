def test_request_validation(client, admin_headers):
    teacher = client.post('/api/teachers', json={
        'full_name': 'Препод',
        'experience': 15,
        'specialty': 'История',
        'department': 'Истфак'
    }, headers=admin_headers).get_json()

    course = client.post('/api/courses', json={
        'title': 'История 101',
        'teacher_id': teacher['id'],
        'student_limit': 1
    }, headers=admin_headers).get_json()

    student1 = client.post('/api/students', json={
        'full_name': 'Первый',
        'email': 'first@student.ru'
    }, headers=admin_headers).get_json()

    r = client.post('/api/requests', json={
        'student_id': student1['id'],
        'course_id': course['id'],
        'status': 'approved'
    }, headers=admin_headers)
    assert r.status_code == 201

    student2 = client.post('/api/students', json={
        'full_name': 'Второй',
        'email': 'second@student.ru'
    }, headers=admin_headers).get_json()

    r2 = client.post('/api/requests', json={
        'student_id': student2['id'],
        'course_id': course['id'],
        'status': 'approved'
    }, headers=admin_headers)
    assert r2.status_code == 400
    assert 'error' in r2.get_json()
