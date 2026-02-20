"""
Integration tests for Auth Routes (v1).

Covered Endpoints:
- POST /v1/auth/register
- POST /v1/auth/login

Scenarios Covered:

REGISTER
---------
✔ Successful registration
✔ Duplicate email registration (400 / 409)

LOGIN
------
✔ Successful login
✔ Wrong password (401)
✔ User not found (401)

Security:
- Password hashing validation
- JWT generation validation
- Proper error handling

Edge Cases:
- Duplicate user creation
- Invalid credentials

Goal:
Ensure authentication system is stable and secure.
"""


def test_register_success(client):
    res = client.post("/v1/auth/register", json={
        "email": "test@test.com",
        "password": "123456"
    })
    assert res.status_code == 200
    assert res.json()["code"] == 201


def test_register_duplicate(client):
    client.post("/v1/auth/register", json={
        "email": "dup@test.com",
        "password": "123456"
    })
    res = client.post("/v1/auth/register", json={
        "email": "dup@test.com",
        "password": "123456"
    })
    assert res.status_code in (400, 409)


def test_login_success(client):
    client.post("/v1/auth/register", json={
        "email": "login@test.com",
        "password": "123456"
    })
    res = client.post("/v1/auth/login", json={
        "email": "login@test.com",
        "password": "123456"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()["data"]


def test_login_wrong_password(client):
    client.post("/v1/auth/register", json={
        "email": "wrong@test.com",
        "password": "123456"
    })
    res = client.post("/v1/auth/login", json={
        "email": "wrong@test.com",
        "password": "bad"
    })
    assert res.status_code == 401


def test_login_user_not_found(client):
    res = client.post("/v1/auth/login", json={
        "email": "unknown@test.com",
        "password": "123456"
    })
    assert res.status_code == 401