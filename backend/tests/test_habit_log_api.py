from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.main import app

# Setup shared in-memory SQLite engine with StaticPool
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_habit_completion_and_streaks():
    print("\n==========================================================")
    print("  HABIT TRACKER - MILESTONE 5 COMPLETION & STREAKS TEST")
    print("==========================================================")

    # 1. Setup User A & User B
    print("\n[Setup] Registering User A & User B...")
    reg_a = client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@test.com", "password": "Password123!"},
    )
    reg_b = client.post(
        "/auth/register",
        json={"username": "bob", "email": "bob@test.com", "password": "Password123!"},
    )
    assert reg_a.status_code == 201
    assert reg_b.status_code == 201

    token_a = client.post(
        "/auth/login", json={"email": "alice@test.com", "password": "Password123!"}
    ).json()["data"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    token_b = client.post(
        "/auth/login", json={"email": "bob@test.com", "password": "Password123!"}
    ).json()["data"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 2. Create Habit for User A
    print("\n[Setup] User A creating habit 'Daily Coding'...")
    res = client.post(
        "/habits",
        json={"title": "Daily Coding", "category": "Learning", "frequency": "daily"},
        headers=headers_a,
    )
    assert res.status_code == 201
    habit_id = res.json()["data"]["id"]

    today = date.today()
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)
    four_days_ago = today - timedelta(days=4)
    five_days_ago = today - timedelta(days=5)
    six_days_ago = today - timedelta(days=6)

    # 3. Mark Completion for 6 days ago, 5 days ago, 4 days ago (Historical 3-day streak)
    print("\n[Test 1] Marking completion for historical dates (6, 5, 4 days ago)...")
    for d in [six_days_ago, five_days_ago, four_days_ago]:
        res = client.post(
            f"/habits/{habit_id}/complete",
            json={"completed_date": str(d)},
            headers=headers_a,
        )
        assert res.status_code == 201

    # 4. Mark Completion for Day Before, Yesterday, Today (Active 3-day streak)
    print("\n[Test 2] Marking completion for day_before, yesterday, and today...")
    for d in [day_before, yesterday, today]:
        res = client.post(
            f"/habits/{habit_id}/complete",
            json={"completed_date": str(d)},
            headers=headers_a,
        )
        assert res.status_code == 201

    # 5. Attempt Duplicate Completion for Today
    print("\n[Test 3] Attempting duplicate completion for today (should return HTTP 400)...")
    res = client.post(
        f"/habits/{habit_id}/complete",
        json={"completed_date": str(today)},
        headers=headers_a,
    )
    print(f" -> Status Code: {res.status_code}")
    print(f" -> Response: {res.json()}")
    assert res.status_code == 400
    assert res.json()["success"] is False

    # 6. Verify Streak Statistics for User A
    print("\n[Test 4] Fetching habit statistics for User A...")
    res = client.get(f"/habits/{habit_id}/stats", headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    print(f" -> Stats Data: {res.json()}")
    assert res.status_code == 200
    stats = res.json()["data"]
    assert stats["current_streak"] == 3  # (day_before, yesterday, today)
    assert stats["longest_streak"] == 3  # Max streak achieved is 3 days
    assert stats["total_completed_days"] == 6
    assert stats["last_completed_date"] == str(today)

    # 7. Fetch Completion History
    print("\n[Test 5] Fetching completion history for User A...")
    res = client.get(f"/habits/{habit_id}/history", headers=headers_a)
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 200
    history = res.json()["data"]
    assert len(history) == 6
    # Verify newest date is first
    assert history[0]["completed_date"] == str(today)
    first_log_id = history[0]["id"]

    # 8. Cross-User Access Isolation: User B attempts access
    print("\n[Test 6] User B attempting to fetch User A's habit stats (should return HTTP 404)...")
    res = client.get(f"/habits/{habit_id}/stats", headers=headers_b)
    assert res.status_code == 404

    print("\n[Test 7] User B attempting to complete User A's habit (should return HTTP 404)...")
    res = client.post(
        f"/habits/{habit_id}/complete",
        json={"completed_date": str(today)},
        headers=headers_b,
    )
    assert res.status_code == 404

    # 9. Delete Today's Log & Re-check Streak Stats
    print("\n[Test 8] User A deleting today's completion log...")
    res = client.delete(
        f"/habits/{habit_id}/complete/{first_log_id}", headers=headers_a
    )
    print(f" -> Status Code: {res.status_code}")
    assert res.status_code == 200

    print("\n[Test 9] Re-checking stats after deleting today's log...")
    res = client.get(f"/habits/{habit_id}/stats", headers=headers_a)
    stats = res.json()["data"]
    # Yesterday is still completed, so current streak remains 2!
    assert stats["current_streak"] == 2
    assert stats["total_completed_days"] == 5

    print("\n==========================================================")
    print("  ✅ ALL HABIT COMPLETION & STREAK TESTS PASSED PERFECTLY!")
    print("==========================================================")


if __name__ == "__main__":
    test_habit_completion_and_streaks()
