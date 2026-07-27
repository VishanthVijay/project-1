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

# Create shared in-memory SQLite engine with StaticPool for test suite
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize tables on test engine
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_habit_crud_flow():
    print("\n==========================================================")
    print("  HABIT TRACKER - MILESTONE 4 HABIT API TEST SUITE")
    print("==========================================================")

    # 1. Setup Two Test Users (User A & User B)
    print("\n[Setup] Registering User A and User B...")
    res_a = client.post(
        "/auth/register",
        json={"username": "user_a", "email": "user_a@test.com", "password": "Password123!"},
    )
    res_b = client.post(
        "/auth/register",
        json={"username": "user_b", "email": "user_b@test.com", "password": "Password123!"},
    )
    assert res_a.status_code == 201
    assert res_b.status_code == 201

    # Login both users to get tokens
    token_a = client.post(
        "/auth/login", json={"email": "user_a@test.com", "password": "Password123!"}
    ).json()["data"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    token_b = client.post(
        "/auth/login", json={"email": "user_b@test.com", "password": "Password123!"}
    ).json()["data"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 2. Test Unauthenticated Requests
    print("\n[Test 1] Attempting to create habit without token...")
    res = client.post("/habits", json={"title": "No Auth Habit"})
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 401

    # 3. Create Habit for User A
    print("\n[Test 2] User A creating a new habit...")
    habit_payload = {
        "title": "Morning Meditation",
        "description": "15 minutes mindfulness",
        "category": "Wellness",
        "frequency": "daily",
    }
    res = client.post("/habits", json=habit_payload, headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    print(f" -> Response: {res.json()}")
    assert res.status_code == 201
    body = res.json()
    assert body["success"] is True
    habit_id = body["data"]["id"]
    assert body["data"]["title"] == "Morning Meditation"

    # 4. Get User A's Habits
    print("\n[Test 3] User A fetching all their habits...")
    res = client.get("/habits", headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 200
    assert len(res.json()["data"]) == 1

    # 5. User B fetches habits (should be empty, cross-user isolation!)
    print("\n[Test 4] User B fetching habits (should return empty list)...")
    res = client.get("/habits", headers=headers_b)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 200
    assert len(res.json()["data"]) == 0

    # 6. Cross-User Access Protection: User B attempts to access User A's habit
    print("\n[Test 5] User B trying to GET User A's habit (should return HTTP 404)...")
    res = client.get(f"/habits/{habit_id}", headers=headers_b)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 404

    print("\n[Test 6] User B trying to UPDATE User A's habit (should return HTTP 404)...")
    res = client.put(f"/habits/{habit_id}", json={"title": "Hacked Title"}, headers=headers_b)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 404

    print("\n[Test 7] User B trying to DELETE User A's habit (should return HTTP 404)...")
    res = client.delete(f"/habits/{habit_id}", headers=headers_b)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 404

    # 7. Update Habit (User A)
    print("\n[Test 8] User A updating their habit...")
    update_payload = {"title": "Evening Meditation", "frequency": "daily"}
    res = client.put(f"/habits/{habit_id}", json=update_payload, headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    print(f" -> Response: {res.json()}")
    assert res.status_code == 200
    assert res.json()["data"]["title"] == "Evening Meditation"

    # 8. Test Invalid Validation (e.g. invalid frequency)
    print("\n[Test 9] Attempting to create habit with invalid frequency...")
    bad_payload = {"title": "Bad Habit", "frequency": "hourly"}
    res = client.post("/habits", json=bad_payload, headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    print(f" -> Response: {res.json()}")
    assert res.status_code == 422

    # 9. Delete Habit (User A)
    print("\n[Test 10] User A deleting their habit...")
    res = client.delete(f"/habits/{habit_id}", headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 200

    # Confirm list is now empty for User A
    res = client.get("/habits", headers=headers_a)
    assert len(res.json()["data"]) == 0

    print("\n==========================================================")
    print("  ✅ ALL HABIT CRUD API TESTS PASSED PERFECTLY!")
    print("==========================================================")


if __name__ == "__main__":
    test_habit_crud_flow()
