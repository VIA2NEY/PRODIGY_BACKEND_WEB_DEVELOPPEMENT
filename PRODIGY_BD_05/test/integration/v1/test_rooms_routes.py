"""
Integration tests for Room Routes (v1).

Covered Endpoints:
- POST   /v1/rooms/hotel/{hotel_id}
- PUT    /v1/rooms/{room_id}
- PATCH  /v1/rooms/{room_id}/availability
- DELETE /v1/rooms/{room_id}
- GET    /v1/rooms/search

RBAC Covered:
--------------
✔ OWNER can create room
✔ USER forbidden to create room (403)
✔ OWNER can update own room
✔ Non-owner cannot update room (403)
✔ OWNER can delete own room
✔ Non-owner cannot delete room (403)

Availability:
--------------
✔ Toggle room availability

Error Handling:
---------------
✔ Room not found (404)
✔ Invalid date range search (400)

Goal:
Ensure room lifecycle management is secure and ownership-protected.
"""



def create_hotel(client, token):
    res = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel R",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.json()["data"]["id"]


def create_room(client, token, hotel_id):
    res = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room 1",
            "description": "Nice",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return res


def test_create_room_success(client, owner_token):
    hotel_id = create_hotel(client, owner_token)

    res = create_room(client, owner_token, hotel_id)
    assert res.status_code == 200

def test_create_room_not_owner(client, user_token):
    res = client.post(
        "/v1/rooms/hotel/123",
        json={
            "title": "Room",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 403


def test_update_room_success(client, owner_token):
    hotel_id = create_hotel(client, owner_token)
    room_id = create_room(client, owner_token, hotel_id).json()["data"]["id"]

    res = client.put(
        f"/v1/rooms/{room_id}",
        json={"title": "Updated"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 200

def test_update_room_not_found(client, owner_token):
    res = client.put(
        "/v1/rooms/11111111-1111-1111-1111-111111111111",
        json={"title": "Updated"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 404

def test_update_room_not_owner(client, user_token):
    res = client.put(
        "/v1/rooms/11111111-1111-1111-1111-111111111111",
        json={"title": "Updated"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 403

def test_toggle_availability(client, owner_token):
    hotel_id = create_hotel(client, owner_token)
    room_id = create_room(client, owner_token, hotel_id).json()["data"]["id"]

    res = client.patch(
        f"/v1/rooms/{room_id}/availability",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 200


def test_delete_room_success(client, owner_token):
    hotel_id = create_hotel(client, owner_token)
    room_id = create_room(client, owner_token, hotel_id).json()["data"]["id"]

    res = client.delete(
        f"/v1/rooms/{room_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 200

def test_delete_room_not_owner(client, owner_token, create_user):
    hotel_id = create_hotel(client, owner_token)
    room_id = create_room(client, owner_token, hotel_id).json()["data"]["id"]

    email, password = create_user("owner")
    login = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    token = login.json()["data"]["access_token"]

    res = client.delete(
        f"/v1/rooms/{room_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403


def test_search_invalid_date(client):
    res = client.get(
        "/v1/rooms/search",
        params={
            "check_in": "2026-05-10",
            "check_out": "2026-05-01"
        }
    )
    assert res.status_code == 400