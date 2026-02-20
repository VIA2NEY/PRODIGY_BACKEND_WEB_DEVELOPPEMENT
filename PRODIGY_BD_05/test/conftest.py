"""
Global pytest configuration for Hotel Booking API.

This file configures:

1. Test Database
   - SQLite in-memory database
   - Fresh schema per test
   - Automatic teardown after each test

2. Redis Mocking
   - FakeRedis class replaces real Redis client
   - Avoids external dependency during tests
   - Simulates get, setex, delete, keys operations

3. FastAPI Dependency Overrides
   - Overrides get_db dependency
   - Injects test database session
   - Clears overrides after test

4. Authentication Fixtures
   - create_user(role): dynamically create user with specific role
   - user_token: returns valid JWT for USER
   - owner_token: returns valid JWT for OWNER
   - admin_token: returns valid JWT for ADMIN

Purpose:
- Ensure test isolation
- Prevent external service usage
- Enable RBAC testing
- Guarantee deterministic results

All integration and e2e tests depend on this setup.
"""


import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db
from app.core.redis import RedisClient

from app.domain.models.users import User
from app.core.security import get_password_hash


# -------------------------
# DATABASE (SQLite memory)
# -------------------------

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def override_get_db(db):
    def _override():
        yield db
    return _override


# -------------------------
# FAKE REDIS
# -------------------------

class FakeRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, ttl, value):
        self.store[key] = value

    def delete(self, *keys):
        for key in keys:
            self.store.pop(key, None)

    def keys(self, pattern):
        return list(self.store.keys())


@pytest.fixture(autouse=True)
def override_redis():
    RedisClient._instance = FakeRedis()
    yield
    RedisClient._instance = None


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = override_get_db(db)
    yield TestClient(app)
    app.dependency_overrides.clear()



# ----------------------
# AUTH FIXTURES
# ----------------------

# def create_user(db, role="user"):
#     email = f"{role}_{uuid.uuid4()}@test.com"
#     password = "123456"

#     user = User(
#         email=email,
#         hashed_password=get_password_hash(password),
#         role=role,
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return email, password

@pytest.fixture
def create_user(db):
    def _create_user(role="user"):
        email = f"{role}_{uuid.uuid4()}@test.com"
        password = "123456"
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return email, password
    return _create_user

@pytest.fixture
def user_token(client, create_user):
    email, password = create_user("user")
    res = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    return res.json()["data"]["access_token"]


@pytest.fixture
def owner_token(client, create_user):
    email, password = create_user("owner")
    res = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    return res.json()["data"]["access_token"]


@pytest.fixture
def admin_token(client, create_user):
    email, password = create_user("admin")
    res = client.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    return res.json()["data"]["access_token"]

