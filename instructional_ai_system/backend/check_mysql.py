import logging
from app.database import SessionLocal
from app.models import User
from app.auth import verify_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SessionLocal()
try:
    users = db.query(User).all()
    for u in users:
        is_valid = verify_password('password123', u.hashed_password)
        logger.info(f"User: {u.email} | Hash: {u.hashed_password[:20]}... | valid for 'password123': {is_valid}")
        is_valid2 = verify_password('password', u.hashed_password)
        logger.info(f"User: {u.email} | Hash: {u.hashed_password[:20]}... | valid for 'password': {is_valid2}")
finally:
    db.close()
