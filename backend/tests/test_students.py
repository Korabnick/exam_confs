def test_student_crud(client, admin_headers):
    create = client.post('/api/students', json={
        'full_name': 'Студент Тестович',
        'email': 'test@student.ru'
    }, headers=admin_headers)
    assert create.status_code == 201
    s_id = create.get_json()['id']

    get = client.get(f'/api/students/{s_id}', headers=admin_headers)
    assert get.status_code == 200

    patch = client.patch(f'/api/students/{s_id}', json={
        'email': 'updated@student.ru'
    }, headers=admin_headers)
    assert patch.status_code == 200

    delete = client.delete(f'/api/students/{s_id}', headers=admin_headers)
    assert delete.status_code == 200
