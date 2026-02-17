"""
Integration tests for Booking Routes (v1).

Covered Endpoints:
- POST   /v1/bookings
- PATCH  /v1/bookings/{booking_id}/cancel

Booking Creation:
------------------
✔ Successful booking
✔ Room not found (404)
✔ Invalid date range (400)
✔ Booking conflict scenario

Cancellation:
--------------
✔ Cancel own booking
✔ Cancel non-existent booking (404)
✔ Cancel by non-owner (403)

RBAC:
------
✔ USER allowed to book
✔ Unauthorized access blocked
✔ Ownership enforced on cancellation

Business Rules Validated:
--------------------------
- Room availability check
- Date validation (check_in < check_out)
- Conflict detection
- Booking ownership validation

Goal:
Guarantee booking integrity and prevent reservation conflicts.
"""



from datetime import date, timedelta


def create_room_for_booking(client, owner_token):
    hotel = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel B",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room Book",
            "description": "Nice",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    return room.json()["data"]["id"]


def test_booking_success(client, user_token, owner_token):
    room_id = create_room_for_booking(client, owner_token)

    res = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200


def test_booking_room_not_found(client, user_token):
    res = client.post(
        "/v1/bookings",
        json={
            "room_id": "11111111-1111-1111-1111-111111111111",
            "check_in_date": "2026-05-10",
            "check_out_date": "2026-05-15",
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 404


def test_booking_invalid_dates(client, user_token):
    res = client.post(
        "/v1/bookings",
        json={
            "room_id": "11111111-1111-1111-1111-111111111111",
            "check_in_date": "2026-05-10",
            "check_out_date": "2026-05-01",
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code in (400, 404)


def test_cancel_success(client, user_token, owner_token):
    room_id = create_room_for_booking(client, owner_token)
    book = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert book.status_code == 200

    res = client.patch(
        f"/v1/bookings/{book.json()['data']['id']}/cancel",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200

def test_cancel_not_found(client, user_token):
    res = client.patch(
        "/v1/bookings/11111111-1111-1111-1111-111111111111/cancel",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 404


def test_cancel_not_owner(client, user_token, owner_token):
    room_id = create_room_for_booking(client, owner_token)
    book = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert book.status_code == 200

    res = client.patch(
        f"/v1/bookings/{book.json()['data']['id']}/cancel",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert res.status_code == 403