# Task-03

## JWT-Based Authentication & Authorization

### Description

Implement authentication and authorization using **JSON Web Tokens (JWT)**.

### Requirements

- Add **user registration** and **login** endpoints.
- Store **hashed passwords** using a library such as **bcrypt**.
- On successful login, **generate and return a JWT token** to the client.
- Protect certain routes (e.g., `/users` or `/profile`) so they are accessible **only by authenticated users** using the JWT token.
- Implement **role-based access control (RBAC)** (e.g., `admin`, `user`, `owner`) to restrict access to specific endpoints.

---