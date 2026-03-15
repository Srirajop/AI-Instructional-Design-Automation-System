import os
import json
from app.services.ai_editing import ai_edit_document
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

storyboard_type2 = """
# STORYBOARD - AI and ML Fundamentals

MODULE 1: Introduction to AI

| Section | Topics | Visual Instructions/Developer Notes | On-screen text | Audio Narration | Status | Actions required |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Intro | What is AI? | • Simple static image | • AI Basics<br>• Definitions | This screen introduces the basic concepts of AI. | Draft | None |
| History | AI History | • Timeline graphic | • 1950s: Turing Test<br>• 1990s: IBM Deep Blue | We will look at the key milestones in AI history. | Draft | Fix bullets |
"""

def test_edit(msg):
    print(f"\nUser Request: {msg}")
    result = ai_edit_document(api_key, storyboard_type2, msg, doc_type="Storyboard Type 2", chat_history=[])
    print(f"Assistant: {result['assistant_reply']}")
    print(f"Is Edit: {result['is_edit']}")
    if result['is_edit']:
        for d in result['diff']:
            print(f"  Changed {d['screen_num']} | {d['col_name']}: '{d['old_content']}' -> '{d['new_content']}'")

if __name__ == "__main__":
    # Test section targeting in Type 2
    test_edit("update the on-screen text for the Intro section to include 'Artificial Intelligence'")
    
    # Test audio narration update
    test_edit("make the audio narration for the History section more exciting")
    
    # Test general chat
    test_edit("looks good")
