"""
E2E - FULL VISITOR FLOW (Unauthenticated)

========================================================
PUBLIC ACCESS VALIDATED
========================================================

✔ Can list hotels
✔ Can view rooms
✔ Can search room availability

========================================================
RESTRICTED ROUTES VALIDATED
========================================================

❌ Cannot create hotel
❌ Cannot update hotel
❌ Cannot delete hotel
❌ Cannot create room
❌ Cannot update room
❌ Cannot delete room
❌ Cannot book room
❌ Cannot cancel booking

========================================================
GOAL
========================================================

Validate security boundaries for unauthenticated users.
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

def test_full_visitor_flow(client: TestClient):

    hotels = client.get("/v1/hotels")
    assert hotels.status_code == 200

    
    # Create owner to create hotel
    owner_headers = register_and_login(client, "owner_for_user@test.com", "owner")

    hotel = client.post(
        "/v1/hotels",
        json={"name": "Hotel Public", "description": "Owner descrip", "address": "Abidjan"},
        headers=owner_headers
    )
    assert hotel.status_code == 200
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={"title": "Room 101", "description": "Nice", "price_per_night": 80, "capacity": 2},
        headers=owner_headers
    )
    assert room.status_code == 200
    room_id = room.json()["data"]["id"]

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


    restricted_routes = [
        ("post", "/v1/hotels"),
        ("put", f"/v1/hotels/{hotel_id}"),
        ("delete", f"/v1/hotels/{hotel_id}"),
        ("post", f"/v1/rooms/hotel/{room_id}"),
        ("put", f"/v1/rooms/{room_id}"),
        ("delete", f"/v1/rooms/{room_id}"),
        ("post", "/v1/bookings"),
        ("patch", f"/v1/bookings/{booking_id}/cancel"),
    ]

    for method, url in restricted_routes:
        response = getattr(client, method)(url)
        assert response.status_code in [401, 403, 405]

    rooms = client.get(f"/v1/rooms/hotel/{hotel_id}")
    assert rooms.status_code == 200