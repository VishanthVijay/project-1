from fastapi import FastAPI

from . import models  # Registers the database tables with SQLAlchemy.
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")


@app.get("/")
def home():
    return {"message": "Habit Tracker API is running"}
