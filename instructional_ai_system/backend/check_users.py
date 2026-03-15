import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("No DATABASE_URL found.")
    exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_users():
    session = SessionLocal()
    from app import models
    users = session.query(models.User).all()
    print(f"Total users found: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Name: {u.name}")
    session.close()

if __name__ == "__main__":
    check_users()
