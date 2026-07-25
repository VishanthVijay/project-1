# Habit Tracker

## Run the backend

1. Open a terminal in `backend`.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it in PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install packages: `pip install -r requirements.txt`
5. Start the API: `uvicorn app.main:app --reload`

Then open `http://127.0.0.1:8000` in your browser. The SQLite database file
`habit_tracker.db` is created inside the `backend` folder automatically.
