import os
import json
from app.services.ai_editing import ai_edit_document
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

design_doc = """
Sample Design Document

# MODULE BREAKDOWN

| Module | Delivery Mode | Learning Objectives | Topics | Recommended Strategy | Activities/Assessment | Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Module 1: Cyber Intro | Self-paced | • Learn basic cyber | AI history | Discussion | MCQ | 1 hr |
| Module 2: Malware | Self-paced | • Understand malware | Viruses, Worms | Interactive Case | Quiz | 2 hrs |
| Module 3: Phishing | Self-paced | • Detect phishing | Spam, Links | Simulation | Performance | 1.5 hrs |
"""

def test_edit(msg):
    print(f"\nUser Request: {msg}")
    result = ai_edit_document(api_key, design_doc, msg, doc_type="Design Document", chat_history=[])
    print(f"Assistant: {result['assistant_reply']}")
    print(f"Is Edit: {result['is_edit']}")
    if result['is_edit']:
        for d in result['diff']:
            print(f"  Changed {d['screen_num']} | {d['col_name']}: '{d['old_content']}' -> '{d['new_content']}'")

if __name__ == "__main__":
    # Test specific module targeting
    test_edit("change the topics of module 2 to 'Viruses, Worms, and Trojans'")
    
    # Test column name resolution
    test_edit("make module 3's strategy more detailed")
    
    # Test general chat in design doc context
    test_edit("thanks for the update")
