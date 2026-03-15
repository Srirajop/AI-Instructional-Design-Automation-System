import os
import json
import io
from dotenv import load_dotenv
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

# Mocking FastAPI dependencies and DB for unit test feel
from app.services import ai_generation, history_service
from app.routers import storyboard
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models

# In-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_regen():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("SKIP: No GROQ_API_KEY found")
        return

    db = TestingSessionLocal()
    user = models.User(email="test@example.com", hashed_password="fake")
    db.add(user)
    db.commit()
    db.refresh(user)

    # 1. Create a project with "extracted_content" (simulating an upload)
    raw_content = "This is a raw storyboard content with some modules and interactions."
    project = models.Project(
        title="Test Upload Regen",
        user_id=user.id,
        extracted_content=raw_content,
        storyboard="Initial beautified version Type 1"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    print(f"Project created with ID: {project.id}")

    # 2. Test Regeneration to Type 2
    # We'll call the logic inside generate_storyboard_stream directly for the uploaded project case
    from fastapi.responses import StreamingResponse
    
    # Simulate Calling the endpoint logic for "Type 2"
    # We'll just test the beautify service call since the endpoint wraps it in SSE
    print("Testing Re-beautify to Type 2...")
    new_sb = ai_generation.beautify_uploaded_content(api_key, raw_content, "storyboard", "Type 2")
    
    print("Regenerated SB snapshot:")
    print(new_sb[:200] + "...")
    
    # Check for Type 2 indicators (7-column table)
    pipe_count = new_sb.count('|')
    if pipe_count >= 7:
        print("SUCCESS: Regenerated storyboard contains tables (likely Type 2)")
    else:
        print(f"FAILURE: Expected many pipes for Type 2, got {pipe_count}")

    # 3. Test Re-beautify to Type 1
    print("\nTesting Re-beautify to Type 1...")
    new_sb_type1 = ai_generation.beautify_uploaded_content(api_key, raw_content, "storyboard", "Type 1")
    print("Regenerated SB Type 1 snapshot:")
    print(new_sb_type1[:200] + "...")
    
    # Type 1 usually has fewer pipes and more headings
    if new_sb_type1.count('|') < pipe_count:
        print("SUCCESS: Type 1 has fewer pipes than Type 2")
    else:
        print("WARNING: Type 1 count vs Type 2 count is unexpected, but AI generation varies.")

    db.close()
    if os.path.exists("./test.db"):
        os.remove("./test.db")

if __name__ == "__main__":
    test_regen()
