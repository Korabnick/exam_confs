def test_create_teacher(client, admin_headers):
    response = client.post('/api/teachers', json={
        'full_name': 'Иван Петров',
        'experience': 5,
        'specialty': 'Математика',
        'department': 'Физико-математический'
    }, headers=admin_headers)
    assert response.status_code == 201

def test_get_teachers(client, admin_headers):
    client.post('/api/teachers', json={
        'full_name': 'Тестовый Препод',
        'experience': 10,
        'specialty': 'Физика',
        'department': 'Физфак'
    }, headers=admin_headers)
    response = client.get('/api/teachers', headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_update_teacher(client, admin_headers):
    post = client.post('/api/teachers', json={
        'full_name': 'Test',
        'experience': 1,
        'specialty': 'Test',
        'department': 'Test'
    }, headers=admin_headers)
    tid = post.get_json()['id']
    response = client.put(f'/api/teachers/{tid}', json={'experience': 10}, headers=admin_headers)
    assert response.status_code == 200

def test_delete_teacher(client, admin_headers):
    post = client.post('/api/teachers', json={
        'full_name': 'To Delete',
        'experience': 1,
        'specialty': 'Test',
        'department': 'Test'
    }, headers=admin_headers)
    tid = post.get_json()['id']
    delete = client.delete(f'/api/teachers/{tid}', headers=admin_headers)
    assert delete.status_code == 200
