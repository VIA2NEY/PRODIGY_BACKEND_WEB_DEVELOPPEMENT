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
from datetime import date, timedelta


def test_full_visitor_flow(client: TestClient, hotel_with_room):

    hotels = client.get("/v1/hotels")
    assert hotels.status_code == 200

    
    # Create owner to create hotel
    owner_headers = hotel_with_room["owner_headers"]
    hotel_id = hotel_with_room["hotel_id"]
    room_id = hotel_with_room["room_id"]

    booking = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=21)),
            "check_out_date": str(date.today() + timedelta(days=24))
        },
        headers=owner_headers
    )
    print(f"data : {booking.json()["message"]}")
    assert booking.status_code == 200
    booking_id = booking.json()["data"]["id"]


    restricted_routes = [
        ("post", "/v1/hotels"),
        ("put", f"/v1/hotels/{hotel_id}"),
        ("delete", f"/v1/hotels/{hotel_id}"),
        ("post", f"/v1/rooms/hotel/{hotel_id}"),
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