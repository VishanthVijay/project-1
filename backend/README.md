# Habit Tracker - Backend API

FastAPI backend application for the Habit Tracker web app. Built with Python, FastAPI, SQLAlchemy ORM, Pydantic, and MySQL.

---

## Prerequisites

- Python 3.10+
- MySQL Server running locally or on a server

---

## Project Structure

```
backend/
├── .env                  # Local environment configuration (Secrets)
├── .gitignore            # Ignored files for Git
├── README.md             # Backend documentation
├── requirements.txt      # Python dependencies
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # App configuration settings loader
│   ├── database/         # Database base & session configuration
│   ├── models/           # SQLAlchemy database ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── routes/           # FastAPI API routers/endpoints
│   ├── services/         # Core business logic handlers
│   └── utils/            # Helper functions (JWT, hashing, dates)
├── migrations/           # Database schema migration scripts (Alembic)
└── tests/                # Automated test suite
```

---

## Setup & Running Locally

### 1. Set Up Virtual Environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create or edit `.env` in `backend/`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=habit_tracker

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload
```

Server will run on: `http://localhost:8000`

---

## Interactive API Documentation (Swagger)

Once the application is running, access:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
