import json

def test_login_success(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_fail_wrong_password(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "wrongpass"
    })
    assert response.status_code == 401
