import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Project

# Connect to the local SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
try:
    project = db.query(Project).first()
    if project:
        print("--- STORYBOARD FROM DB ---")
        print(project.storyboard)
        with open("db_storyboard_dump.txt", "w", encoding="utf-8") as f:
            f.write(project.storyboard)
    else:
        print("No project found in DB.")
finally:
    db.close()
