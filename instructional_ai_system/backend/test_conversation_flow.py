import os
import json
from app.services.ai_editing import ai_edit_document
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

mock_doc = """
Screen 1.1 Title: Introduction
| ON-SCREEN TEXT (OST) | AUDIO NARRATION | VISUAL INSTRUCTIONS & DEVELOPER NOTES |
| :--- | :--- | :--- |
| Welcome to the course. | Hello everyone. | Introductory slide. |

Screen 1.2 Title: Safety Protocols
| ON-SCREEN TEXT (OST) | AUDIO NARRATION | VISUAL INSTRUCTIONS & DEVELOPER NOTES |
| :--- | :--- | :--- |
| Safety first. | Always remember safety. | Safety icon. |
"""

def test_chat(msg):
    print(f"\nUser: {msg}")
    result = ai_edit_document(api_key, mock_doc, msg, chat_history=[])
    print(f"Assistant: {result['assistant_reply']}")
    print(f"Is Edit: {result['is_edit']}")

if __name__ == "__main__":
    test_chat("Hello, how are you today?")
    test_chat("Thanks for the help!")
    test_chat("Can you change Screen 1.1's OST to 'Welcome to the Safety Course'?")
