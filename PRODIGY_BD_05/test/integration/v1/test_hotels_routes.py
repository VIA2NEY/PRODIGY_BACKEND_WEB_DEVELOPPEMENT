"""
Integration tests for Hotel Routes (v1).

Covered Endpoints:
- POST   /v1/hotels
- PUT    /v1/hotels/{hotel_id}
- GET    /v1/hotels

RBAC Covered:
--------------
✔ OWNER can create hotel
✔ ADMIN can create hotel
✔ USER forbidden to create hotel (403)

Update Scenarios:
-----------------
✔ Update success (owner)
✔ Update hotel not found (404)
✔ Update by non-owner (403)

Listing:
--------
✔ List hotels (public access)

Security Validation:
- Role-based access control
- Ownership validation
- Resource existence check

Goal:
Guarantee RBAC correctness and hotel ownership integrity.
"""

def create_hotel(client, token):
    res = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel A",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return res


def test_create_hotel_owner(client, owner_token):
    res = create_hotel(client, owner_token)
    assert res.status_code == 200


def test_create_hotel_admin(client, admin_token):
    res = create_hotel(client, admin_token)
    assert res.status_code == 200


def test_create_hotel_forbidden_user(client, user_token):
    res = create_hotel(client, user_token)
    assert res.status_code == 403


def test_update_hotel_not_found(client, owner_token):
    res = client.put(
        "/v1/hotels/11111111-1111-1111-1111-111111111111",
        json={"name": "Updated"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 404


def test_update_hotel_success(client, owner_token):
    res = create_hotel(client, owner_token)
    hotel_id = res.json()["data"]["id"]

    res = client.put(
        f"/v1/hotels/{hotel_id}",
        json={"name": "Updated"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 200

def test_update_hotel_not_owner(client, owner_token, create_user):
    # create hotel with first owner
    res = create_hotel(client, owner_token)
    hotel_id = res.json()["data"]["id"]

    # new owner
    email, password = create_user("owner")
    login = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    new_token = login.json()["data"]["access_token"]

    res = client.put(
        f"/v1/hotels/{hotel_id}",
        json={"name": "Hack"},
        headers={"Authorization": f"Bearer {new_token}"}
    )
    assert res.status_code == 403


def test_list_hotels(client):
    res = client.get("/v1/hotels")
    assert res.status_code == 200