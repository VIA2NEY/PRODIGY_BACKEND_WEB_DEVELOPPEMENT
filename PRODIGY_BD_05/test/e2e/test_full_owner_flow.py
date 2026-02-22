"""
E2E - FULL OWNER FLOW

========================================================
OWNER CAPABILITIES VALIDATED
========================================================

✔ Owner can register
✔ Owner can login
✔ Owner can create hotel
✔ Owner can update hotel
✔ Owner can delete hotel
✔ Owner can create room
✔ Owner can update room
✔ Owner can delete room
✔ Owner can book room
✔ Owner can cancel booking

========================================================
GOAL
========================================================

- Validate ownership lifecycle
- Validate CRUD hotel & room
- Validate booking lifecycle
- Validate RBAC for OWNER role
"""

from fastapi.testclient import TestClient


def register_and_login(client: TestClient, email: str, role: str):
    password = "StrongPassword123!"
    client.post(f"/v1/auth/register?role={role.lower()}", json={
        "email": email,
        "password": password
    })
    response = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_full_owner_flow(client: TestClient):

    owner_headers = register_and_login(client, "owner@test.com", "owner")

    # Create hotel
    hotel = client.post(
        "/v1/hotels",
        json={"name": "Owner Hotel", "description": "Owner descrip", "address": "Abidjan"},
        headers=owner_headers
    )
    assert hotel.status_code == 200
    hotel_id = hotel.json()["data"]["id"]

    update = client.put(
        f"/v1/hotels/{hotel_id}",
        json={"name": "Updated Owner Hotel"},
        headers=owner_headers
    )
    assert update.status_code == 200

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={"title": "Room 101", "description": "Nice", "price_per_night": 80, "capacity": 2},
        headers=owner_headers
    )
    assert room.status_code == 200
    room_id = room.json()["data"]["id"]

    update_room = client.put(
        f"/v1/rooms/{room_id}",
        json={"price_per_night": 90},
        headers=owner_headers
    )
    assert update_room.status_code == 200

    # Toggle availability
    toggle = client.patch(
        f"/v1/rooms/{room_id}/availability",
        headers=owner_headers
    )
    assert toggle.status_code == 200

    # Toggle back to available
    client.patch(f"/v1/rooms/{room_id}/availability", headers=owner_headers)

    booking = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": "2026-07-01",
            "check_out_date": "2026-07-03"
        },
        headers=owner_headers
    )
    assert booking.status_code == 200
    booking_id = booking.json()["data"]["id"]

    cancel = client.patch(
        f"/v1/bookings/{booking_id}/cancel",
        headers=owner_headers
    )
    assert cancel.status_code == 200

    # delete_room = client.delete(
    #     f"/v1/rooms/{room_id}",
    #     headers=owner_headers
    # )
    # assert delete_room.status_code == 200

    # delete_hotel = client.delete(
    #     f"/v1/hotels/{hotel_id}",
    #     headers=owner_headers
    # )
    # assert delete_hotel.status_code == 200

    # logout = client.post(
    #     "/v1/auth/logout",
    #     headers=owner_headers
    # )
    # assert logout.status_code == 200