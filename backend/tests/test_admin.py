def test_admin_index_accessible(client):
    resp = client.get("/admin/")
    assert resp.status_code == 200
    assert b'Exam Admin' in resp.data

def test_admin_model_views_exist(client):
    resp = client.get("/admin/")
    html = resp.data.decode('utf-8')
    for name in ("Teacher", "Course", "Student", "Request"):
        assert name in html
