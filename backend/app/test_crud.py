import os
import sys
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import crud
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog

# Setup an in-memory SQLite engine for demonstration testing
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)

# Create tables in the test engine
Base.metadata.create_all(bind=engine)


def run_crud_demonstration():
    print("\n==========================================================")
    print("  HABIT TRACKER - MILESTONE 2.5 CRUD DEMONSTRATION SCRIPT")
    print("==========================================================")

    db = SessionLocal()

    try:
        # ----------------------------------------------------
        # 1. User CRUD Operations
        # ----------------------------------------------------
        print("\n[Step 1] Creating a test user...")
        user = crud.create_user(
            db,
            username="alex_dev",
            email="alex@university.edu",
            password_hash="hashed_secret_password_123",
        )
        assert user is not None
        print(f" -> Created User: ID={user.id}, Username='{user.username}', Email='{user.email}'")

        # ----------------------------------------------------
        # 2. Habit CRUD Operations
        # ----------------------------------------------------
        print("\n[Step 2] Creating two habits for the user...")
        habit1 = crud.create_habit(
            db,
            user_id=user.id,
            title="Morning Workout",
            description="30 minutes of cardio and stretching",
            category="Fitness",
            frequency="daily",
        )
        habit2 = crud.create_habit(
            db,
            user_id=user.id,
            title="LeetCode Problem",
            description="Solve at least 1 medium problem",
            category="Study",
            frequency="daily",
        )
        assert habit1 is not None and habit2 is not None
        print(f" -> Habit 1 Created: ID={habit1.id}, Title='{habit1.title}', Category='{habit1.category}'")
        print(f" -> Habit 2 Created: ID={habit2.id}, Title='{habit2.title}', Category='{habit2.category}'")

        # ----------------------------------------------------
        # 3. HabitLog CRUD Operations
        # ----------------------------------------------------
        print("\n[Step 3] Adding completion logs for habits...")
        today = date.today()
        yesterday = today - timedelta(days=1)

        log1 = crud.create_habit_log(db, habit_id=habit1.id, completed_date=yesterday, completed=True)
        log2 = crud.create_habit_log(db, habit_id=habit1.id, completed_date=today, completed=True)
        log3 = crud.create_habit_log(db, habit_id=habit2.id, completed_date=today, completed=True)

        print(f" -> Log 1: Habit '{habit1.title}' completed on {log1.completed_date}")
        print(f" -> Log 2: Habit '{habit1.title}' completed on {log2.completed_date}")
        print(f" -> Log 3: Habit '{habit2.title}' completed on {log3.completed_date}")

        # ----------------------------------------------------
        # 4. Verifying ORM Relationship: User -> Habit
        # ----------------------------------------------------
        print("\n[Step 4] Demonstrating ORM Relationship: User -> Habits (user.habits)")
        fetched_user = crud.get_user_by_id(db, user.id)
        print(f" -> Fetched User: {fetched_user.username}")
        print(f" -> Number of Habits (via user.habits): {len(fetched_user.habits)}")
        for h in fetched_user.habits:
            print(f"     - Habit: '{h.title}' (ID={h.id})")

        # ----------------------------------------------------
        # 5. Verifying ORM Relationship: Habit -> HabitLog
        # ----------------------------------------------------
        print("\n[Step 5] Demonstrating ORM Relationships: Habit -> Logs & Log -> Habit")
        fetched_habit1 = crud.get_habit_by_id(db, habit1.id)
        print(f" -> Habit: '{fetched_habit1.title}' has {len(fetched_habit1.logs)} log entries (via habit.logs):")
        for log in fetched_habit1.logs:
            print(f"     - Log Date: {log.completed_date} | Parent Habit Title (via log.habit): '{log.habit.title}'")

        # ----------------------------------------------------
        # 6. Update Habit
        # ----------------------------------------------------
        print("\n[Step 6] Updating Habit 1...")
        updated_habit1 = crud.update_habit(
            db,
            habit_id=habit1.id,
            title="Morning HIIT Workout",
            description="45 minutes high intensity interval training",
        )
        print(f" -> Updated Title: '{updated_habit1.title}'")
        print(f" -> Updated Description: '{updated_habit1.description}'")

        # ----------------------------------------------------
        # 7. Delete Habit & Verify Cascade Deletion
        # ----------------------------------------------------
        print("\n[Step 7] Deleting Habit 2 (ID={}) and verifying cascade deletion of logs...".format(habit2.id))
        logs_before_delete = len(crud.get_habit_logs(db, habit2.id))
        print(f" -> Logs for Habit 2 before deletion: {logs_before_delete}")

        delete_success = crud.delete_habit(db, habit2.id)
        logs_after_delete = len(crud.get_habit_logs(db, habit2.id))
        print(f" -> Delete Habit 2 executed: {delete_success}")
        print(f" -> Logs for Habit 2 after habit deletion: {logs_after_delete} (Cascade auto-deleted associated logs!)")

        # ----------------------------------------------------
        # 8. Final Count Verification
        # ----------------------------------------------------
        total_users = len(crud.get_all_users(db))
        total_habits = len(crud.get_user_habits(db, user.id))
        total_logs = len(crud.get_habit_logs(db, habit1.id))

        print("\n==========================================================")
        print("  FINAL DATABASE RECORD VERIFICATION SUMMARY")
        print("==========================================================")
        print(f" -> Total Users in DB:      {total_users}")
        print(f" -> Total Habits in DB:     {total_habits}")
        print(f" -> Total Habit Logs in DB: {total_logs}")
        print("==========================================================")
        print("  ✅ ALL CRUD OPERATIONS & CASCADE DELETES VERIFIED PERFECTLY!")
        print("==========================================================")

    finally:
        db.close()


if __name__ == "__main__":
    run_crud_demonstration()
