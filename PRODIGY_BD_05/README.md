# Task 05 – Hotel Booking Platform Backend API (Mini Project)

## Description
Develop a backend API for a **hotel booking platform** that provides core functionalities for managing hotel room listings, searching availability, and booking rooms securely.

This mini-project focuses on backend fundamentals such as authentication, relational databases, validation, and error handling.

---

## Objectives
- Build a scalable and secure backend API
- Enable users to manage hotel room listings
- Allow users to search, filter, and book available rooms
- Implement authentication and proper data validation

---

## Requirements

### 1. User Hotel Room Management
- Provide endpoints for users to:
  - Create hotel room listings
  - Edit their own hotel room listings
  - Delete their own hotel room listings

---

### 2. Search & Filter Available Rooms
- Add endpoints to:
  - Search available hotel rooms
  - Filter rooms based on criteria such as:
    - Check-in date
    - Check-out date

---

### 3. Room Booking Functionality
- Implement room booking features where:
  - Users can reserve available hotel rooms
  - Booking conflicts are prevented
  - Availability is correctly managed

---

### 4. Authentication & Security
- Ensure secure access to user accounts using authentication
- Use **JWT (JSON Web Tokens)** or equivalent authentication mechanisms
- Protect sensitive endpoints

---

### 5. Database
- Use a **relational database** such as:
  - PostgreSQL
  - MySQL
- Store:
  - User accounts
  - Hotel room details
  - Booking records

---

### 6. Validation & Error Handling
- Add input validation for all endpoints
- Implement proper and consistent error handling
- Return meaningful HTTP status codes and messages

---

## Technologies (Suggested)
- Backend Framework: FastAPI
- Authentication: JWT
- Database: PostgreSQL / MySQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Testing: Pytest

---

## Notes
This project builds upon previous tasks by introducing more complex business logic, data relationships, and security considerations while maintaining clean architecture principles.

---

# APP ARCHITECTURE

```
├── alembic/ 
│   ├── env.py
│   └── ...
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── router.py              # Inclut v1 et v2
│   │   │
│   │   ├── v1/
│   │   │   ├── dependencies.py
│   │   │   ├── schemas/
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── hotels.py
│   │   │       ├── rooms.py
│   │   │       └── bookings.py
│   │   │
│   │   └── v2/
│   │       ├── dependencies.py
│   │       └── routes/
│   │           ├── hotels.py
│   │           └── bookings.py
│   │
│   ├── application/
│   │   └── services/
│   │       ├── v1/
│   │       │   ├── auth_service.py
│   │       │   ├── hotel_service.py
│   │       │   └── booking_service.py
│   │       │
│   │       └── v2/
│   │       ├── hotel_service.py   # logique différente
│   │       └── booking_service.py
│   │
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   │
│   │   └── repositories/
│   │       ├── user_repository.py
│   │       ├── hotel_repository.py
│   │       └── booking_repository.py
│   │
│   ├── domain/
│   │   └── models/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── redis.py
│   │   └── exceptions.py
│   │
│   ├── utils/
│   │   └── response.py
│   │
│
├── tests/
|   │
|   ├── conftest.py          # config globale pytest
|   │
|   ├── unit/
|   │   ├── test_auth_service.py
|   │   ├── test_hotel_service.py
|   │   └── test_booking_service.py
|   │
|   ├── integration/
|   │   ├── v1/
|   │   │   ├── test_auth_routes.py
|   │   │   ├── test_bookings_routes.py
|   │   │   └── test_hotels_routes.py
|   │   │
|   │   └── v2/
|   │       ├── ...
|   │       └── ...
|   │
|   └── e2e/
|   │   ├── test_full_admin_flow.py
|   │   ├── test_full_owner_flow.py
|   │   ├── test_full_user_flow.py
|   │   └── test_full_visitor_flow.py

├── requirements.txt
├── alembic.ini
├── ...
└── README.md

```

## EFFECTUER LES TESTS
- Test Simples
```bash
pytest -v
```

- Test avec Coverage :
```
pytest --cov=app --cov-report=term-missing
```

- Test avec Coverage HTML :
```
pytest --cov=app --cov-report=html
```

- Test simple avec HTML :
```
pytest --cov=app --cov-report=html -v
```

- Test d'ensemble specifique:
```
pytest -k e2e -v
```
ou 
```
pytest -k integration -v
```
## COMMON HTTP RESPONSE CODES


<details>
<summary>HTTP Status Codes in FastAPI</summary>

| Status Code | Name               | Description                                                                 | When to use in FastAPI                                             |
|-------------|--------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------|
| 400         | Bad Request        | The server cannot process the request due to invalid client-side syntax or general errors.  | For generic client errors not covered by 422 validation errors.   |
| 401         | Unauthorized       | The client must authenticate to get the requested response.               | When authentication credentials are missing or invalid.           |
| 403         | Forbidden          | The client does not have permission to access the content, even with authentication.                | For authorization (permissions) issues.                           |
| 404         | Not Found          | The server cannot find the requested resource.                            | When a specific item or endpoint does not exist.                  |
| 405         | Method Not Allowed | The request method is not supported for the target resource.              | When using the wrong HTTP method (e.g., GET instead of POST).     |
| 409         | Conflict           | The request conflicts with the current state of the server.              | For issues like duplicate entries.                               |
| 422         | Unprocessable Entity| The server understands the request but cannot process it due to semantic errors in the data.                | This is common for Pydantic validation errors.                                  |
| 500         | Internal Server Error| The server encountered an unexpected condition.                          | For unhandled exceptions in your code (e.g., a ZeroDivisionError). |
</details>