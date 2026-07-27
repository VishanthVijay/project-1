import sys
from datetime import date
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Create an in-memory SQLite engine to verify schemas and relationships independently
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)

from app.database import Base
from app.models import User, Habit, HabitLog

print("--- 1. Creating database tables in memory ---")
Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Generated Tables: {tables}")

for table_name in ["users", "habits", "habit_logs"]:
    print(f"\nStructure for table '{table_name}':")
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"  - Column: {col['name']} | Type: {col['type']} | Nullable: {col['nullable']}")
    
    fks = inspector.get_foreign_keys(table_name)
    if fks:
        for fk in fks:
            print(f"  - Foreign Key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

print("\n--- 2. Testing Relationships & Cascades ---")
db = SessionLocal()

# Create dummy user
user = User(
    username="cs_student",
    email="student@university.edu",
    password_hash="hashed_secret_123"
)
db.add(user)
db.commit()
db.refresh(user)
print(f"Created User: {user}")

# Create dummy habit using relationship link
habit = Habit(
    title="Read CS Textbook",
    description="30 minutes of algorithms daily",
    category="Study",
    frequency="daily",
    user=user  # ORM relationship assignment
)
db.add(habit)
db.commit()
db.refresh(habit)
print(f"Created Habit: {habit}")

# Create habit log entry
log = HabitLog(
    habit=habit,
    completed_date=date.today(),
    completed=True
)
db.add(log)
db.commit()

print(f"User's habits via ORM relationship: {user.habits}")
print(f"Habit's logs via ORM relationship: {habit.logs}")
print(f"Log's parent habit via ORM relationship: {log.habit.title}")

# Verify cascade delete: deleting user deletes habits & logs automatically
db.delete(user)
db.commit()

remaining_habits = db.query(Habit).all()
remaining_logs = db.query(HabitLog).all()

print(f"\nAfter deleting user:")
print(f"Remaining Habits in DB: {len(remaining_habits)}")
print(f"Remaining Logs in DB: {len(remaining_logs)}")

if len(remaining_habits) == 0 and len(remaining_logs) == 0:
    print("\n✅ Success! All models, relationships, foreign keys, and cascades verified working perfectly!")
else:
    print("\n❌ Failure in relationship cascade verification.")
    sys.exit(1)
