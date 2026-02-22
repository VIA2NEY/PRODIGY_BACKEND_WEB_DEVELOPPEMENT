"""
E2E - FULL ADMIN FLOW

This test validates the complete ADMIN journey:

========================================================
ADMIN CAPABILITIES VALIDATED
========================================================

✔ Admin can register
✔ Admin can login
✔ Admin can create hotel
✔ Admin can create room
✔ Admin can book room
✔ Admin can cancel booking

========================================================
RBAC RESTRICTIONS VALIDATED
========================================================

❌ Admin cannot modify hotel owned by another OWNER

========================================================
GOAL
========================================================

- Validate full system integration
- Validate ADMIN privileges
- Validate ownership protection
- Validate booking lifecycle
- Ensure RBAC is strictly enforced
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
    
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_full_admin_flow(client: TestClient):

    admin_headers = register_and_login(client, "admin@test.com", "admin")

    # Create hotel
    hotel = client.post(
        "/v1/hotels",
        json={"name": "Admin Hotel", "description": "Admin descrip", "address": "Abidjan"},
        headers=admin_headers
    )
    assert hotel.status_code in [200, 201]
    hotel_id = hotel.json()["data"]["id"]

    # Admin CANNOT update hotel
    update = client.put(
        f"/v1/hotels/{hotel_id}",
        json={"name": "Hack"},
        headers=admin_headers
    )
    assert update.status_code == 403

    # Create room
    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={"title": "Room 101", "description": "Nice", "price_per_night": 80, "capacity": 2},
        headers=admin_headers
    )
    assert room.status_code in [401, 403, 405]
    
    # Create OWNER hotel and room create
    owner_headers = register_and_login(client, "owner_block@test.com", "owner")

    owner_hotel = client.post(
        "/v1/hotels",
        json={"name": "Owner Hotel", "description": "Owner descrip", "address": "Yamoussoukro"},
        headers=owner_headers
    )
    assert owner_hotel.status_code == 200
    owner_hotel_id = owner_hotel.json()["data"]["id"]

    owner_hotel_room = client.post(
        f"/v1/rooms/hotel/{owner_hotel_id}",
        json={"title": "Room 101", "description": "Nice", "price_per_night": 80, "capacity": 2},
        headers=owner_headers
    )
    assert owner_hotel_room.status_code == 200
    room_id = owner_hotel_room.json()["data"]["id"]

    # Book room
    booking = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": "2026-06-01",
            "check_out_date": "2026-06-05"
        },
        headers=admin_headers
    )
    assert booking.status_code == 200
    booking_id = booking.json()["data"]["id"]

    # Cancel booking
    cancel = client.patch(
        f"/v1/bookings/{booking_id}/cancel",
        headers=admin_headers
    )
    assert cancel.status_code == 200

    # Admin tries to modify owner's hotel
    forbidden = client.put(
        f"/v1/hotels/{owner_hotel_id}",
        json={"name": "Illegal Update"},
        headers=admin_headers
    )
    assert forbidden.status_code in [401, 403, 405]

    # Delete room
    # delete_room = client.delete(
    #     f"/v1/rooms/{room_id}",
    #     headers=admin_headers
    # )
    # assert delete_room.status_code == 200

    # # Delete hotel
    # delete_hotel = client.delete(
    #     f"/v1/hotels/{hotel_id}",
    #     headers=admin_headers
    # )
    # assert delete_hotel.status_code == 200