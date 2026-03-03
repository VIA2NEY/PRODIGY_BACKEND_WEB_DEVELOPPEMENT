"""
Integration tests for Cache Behavior (v1).

Covered Endpoints:
- GET /v1/rooms/search

Cache Behavior:
---------------
✔ Cache is used for the first request
✔ Cache is not used for subsequent requests

Goal:
Ensure that the cache is used for the first request and not for subsequent requests.
"""



from datetime import date, timedelta


def test_search_rooms_cache_usage(client, owner_token):
    # Setup
    hotel = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel Cache",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room Cache",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    params = {
        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=3)),
    }

    # 1er appel → DB
    res1 = client.get("/v1/rooms/search", params=params)
    assert res1.status_code == 200
    assert len(res1.json()["data"]) == 1

    # 2e appel → cache
    res2 = client.get("/v1/rooms/search", params=params)
    assert res2.status_code == 200
    assert res2.json() == res1.json()


def test_cache_invalidated_after_booking(client, owner_token, user_token):
    # Setup
    hotel = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel Invalidation",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room Invalidation",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    room_id = room.json()["data"]["id"]

    params = {
        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=3)),
    }

    # 1️⃣ Search → cache rempli
    res1 = client.get("/v1/rooms/search", params=params)
    assert len(res1.json()["data"]) == 1

    # 2️⃣ Booking
    book = client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": params["check_in"],
            "check_out_date": params["check_out"],
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert book.status_code == 200

    # 3️⃣ Search après booking
    res2 = client.get("/v1/rooms/search", params=params)

    # 🔥 La room ne doit plus apparaître
    assert res2.status_code == 200
    assert len(res2.json()["data"]) == 0

def test_search_no_500_after_booking(client, owner_token, user_token):
    hotel = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel Stability",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room Stable",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    room_id = room.json()["data"]["id"]

    params = {
        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=3)),
    }

    client.get("/v1/rooms/search", params=params)

    client.post(
        "/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": params["check_in"],
            "check_out_date": params["check_out"],
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # 3 Appel répété
    for _ in range(3):
        res = client.get("/v1/rooms/search", params=params)
        assert res.status_code == 200

    # 4 Appel répété hotel
    for _ in range(3):
        res = client.get("/v1/hotels")
        assert res.status_code == 200

    # 5 Appel répété room available
    for _ in range(3):
        res = client.get("/v1/rooms/available")
        assert res.status_code == 200

def test_cache_invalidated_after_room_update(client, owner_token):
    # Setup
    hotel = client.post(
        "/v1/hotels",
        json={
            "name": "Hotel Update",
            "description": "Nice",
            "address": "Paris"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    hotel_id = hotel.json()["data"]["id"]

    room = client.post(
        f"/v1/rooms/hotel/{hotel_id}",
        json={
            "title": "Room Update",
            "price_per_night": 100,
            "capacity": 2
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    room_id = room.json()["data"]["id"]

    params = {
        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=3)),
    }

    # 1️⃣ Search → cache rempli
    res1 = client.get("/v1/rooms/search", params=params)
    assert len(res1.json()["data"]) == 1

    # 2️⃣ Room update
    client.put(
        f"/v1/rooms/{room_id}",
        json={
            "title": "Room Updated",
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    # 3️⃣ Search après room update
    res2 = client.get("/v1/rooms/search", params=params)
    
    # La room ne doit plus apparaître
    assert res2.status_code == 200
    assert len(res2.json()["data"]) == 1
    assert res2.json()["data"][0]["id"] == room_id
    
    for _ in range(3):
        res_room = client.get(f"/v1/rooms/search?check_in={str(date.today())}&check_out={str(date.today() + timedelta(days=7))}")
        assert res_room.status_code == 200

