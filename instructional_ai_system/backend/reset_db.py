from app.database import engine
from app.models import Base

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("Creating all tables from current models...")
Base.metadata.create_all(bind=engine)
print("Done.")
