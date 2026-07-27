import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.main import app

# Create shared in-memory SQLite engine with StaticPool so all sessions share the same DB tables
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables on the testing engine
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_auth_flow():
    print("\n==========================================================")
    print("  HABIT TRACKER - STANDARDIZED AUTHENTICATION TEST SUITE")
    print("==========================================================")

    # 1. Register User
    print("\n[Test 1] Registering a new user...")
    register_payload = {
        "username": "sarah_connor",
        "email": "sarah@cyberdyne.com",
        "password": "Terminator123!"
    }
    response = client.post("/auth/register", json=register_payload)
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["username"] == "sarah_connor"
    assert "password_hash" not in body["data"]

    # 2. Test Duplicate Email
    print("\n[Test 2] Attempting registration with duplicate email...")
    dup_email_payload = {
        "username": "sarah_alt",
        "email": "sarah@cyberdyne.com",
        "password": "AnotherPassword"
    }
    response = client.post("/auth/register", json=dup_email_payload)
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert "already exists" in body["message"]

    # 3. Login with Invalid Password
    print("\n[Test 3] Attempting login with incorrect password...")
    wrong_login = {
        "email": "sarah@cyberdyne.com",
        "password": "WrongPassword"
    }
    response = client.post("/auth/login", json=wrong_login)
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False

    # 4. Login with Valid Credentials
    print("\n[Test 4] Logging in with correct credentials...")
    valid_login = {
        "email": "sarah@cyberdyne.com",
        "password": "Terminator123!"
    }
    response = client.post("/auth/login", json=valid_login)
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    token = body["data"]["access_token"]

    # 5. Access Protected /auth/me without token
    print("\n[Test 5] Accessing protected /auth/me without Bearer token...")
    response = client.get("/auth/me")
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 401

    # 6. Access Protected /auth/me with valid Bearer token
    print("\n[Test 6] Accessing protected /auth/me with valid Bearer token...")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    print(f" -> Status Code: {response.status_code}")
    print(f" -> Response Body: {response.json()}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "sarah@cyberdyne.com"
    assert body["data"]["username"] == "sarah_connor"

    print("\n==========================================================")
    print("  ✅ ALL STANDARDIZED AUTHENTICATION TESTS PASSED PERFECTLY!")
    print("==========================================================")


if __name__ == "__main__":
    test_auth_flow()
