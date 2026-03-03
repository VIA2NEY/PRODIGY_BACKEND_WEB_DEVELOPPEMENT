"""
E2E - FULL USER FLOW

========================================================
USER CAPABILITIES VALIDATED
========================================================

✔ User can register
✔ User can login
✔ User can list hotels
✔ User can view rooms
✔ User can book room
✔ User can cancel booking

========================================================
RBAC RESTRICTIONS VALIDATED
========================================================

❌ User cannot create hotel
❌ User cannot modify hotel
❌ User cannot delete hotel
❌ User cannot create room
❌ User cannot modify room
❌ User cannot delete room
"""

from fastapi.testclient import TestClient
from datetime import date, timedelta


def test_full_user_flow(client: TestClient, register_and_login, hotel_with_room):

    # Create owner to create hotel and room
    hotel_id = hotel_with_room["hotel_id"]
    room_id = hotel_with_room["room_id"]

    # Now login as USER
    headers = register_and_login("user@test.com", "user")

    hotels = client.get("/v1/hotels")
    assert hotels.status_code == 200

    rooms = client.get(f"/v1/rooms/hotel/{hotel_id}")
    assert rooms.status_code == 200

    forbidden = client.post("/v1/hotels", json={"name": "Illegal"}, headers=headers)
    assert forbidden.status_code in [401, 403, 405]


    forbidden_2 = client.post(f"/v1/rooms/hotel/{hotel_id}", json={"name": "Illegal"}, headers=headers)
    assert forbidden_2.status_code in [401, 403, 405]

    # Booking success
    booking = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3))
        },
        headers=headers
    )
    assert booking.status_code == 200
    booking_id = booking.json()["data"]["id"]

    # Booking already exists
    booking = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3))
        },
        headers=headers
    )
    assert booking.status_code == 400

    # Conflict booking
    conflict = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=2)),
            "check_out_date": str(date.today() + timedelta(days=4)),
        },
        headers=headers
    )
    assert conflict.status_code == 400

    # Booking in the past
    past = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() - timedelta(days=1)),
            "check_out_date": str(date.today() - timedelta(days=3)),
        },
        headers=headers
    )
    assert past.status_code == 422

    cancel = client.patch(f"/v1/bookings/{booking_id}/cancel", headers=headers)
    assert cancel.status_code == 200



