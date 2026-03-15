import os
from dotenv import load_dotenv
from app.services.ai_generation import beautify_uploaded_content

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def test_upload_fix():
    print("Testing Storyboard Type 1 (3-column) Upload...")
    type1_raw = """
Screen 1.1 Title: Introduction
| On-Screen Text (OST) | Audio Narration | Visual Instructions & Developer Notes |
| • Welcome to the course | Hello everyone, welcome to the training. | • Show company logo at the center.<br>• Play intro music. |
"""
    result1 = beautify_uploaded_content(api_key, type1_raw, "storyboard")
    if "| Audio Narration | Visual Instructions & Developer Notes |" in result1:
        print("SUCCESS_TYPE_1")
    
    print("\nTesting Storyboard Type 2...")
    type2_raw = """
| Section | Topics | Visual Instructions/Developer Notes | On-screen text | Audio Narration | Status | Actions required |
| Intro | Course Overview | • Module listing on screen. | • Welcome | Welcome to the training. | Draft | None |
"""
    result2 = beautify_uploaded_content(api_key, type2_raw, "storyboard")
    if "| On-screen text | Audio Narration | Status |" in result2:
        print("SUCCESS_TYPE_2")
    else:
        print("FAILURE")
        print(f"Result count: {result2.count('|')}")

if __name__ == "__main__":
    test_upload_fix()
