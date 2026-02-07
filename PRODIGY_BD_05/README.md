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
