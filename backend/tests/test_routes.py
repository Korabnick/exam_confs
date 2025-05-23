def test_get_teachers(client):
    response = client.get('/api/teachers', headers={'Authorization': 'Basic ...'})
    assert response.status_code == 200
