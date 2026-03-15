import sys
import os
import json
import re

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_editing import ai_edit_document

# Load current storyboard
with open('backend/current_storyboard.txt', 'r', encoding='utf-8') as f:
    current_doc = f.read()

# Prompt from screenshot
user_instruction = "Please change screen 1.1 ost"
api_key = os.environ.get("GROQ_API_KEY")

print(f"Simulating: {user_instruction}")

try:
    # We pass an empty chat history for simplicity, 
    # but the AI knows what Screen 1.1 is from the prompt.
    result = ai_edit_document(api_key, current_doc, user_instruction, "Storyboard", [])
    
    # Check if a log was created
    if os.path.exists("edit_debug.log"):
        with open("edit_debug.log", "r", encoding="utf-8") as f:
            print("\n--- DEBUG LOG CONTENT ---")
            print(f.read())
    else:
        print("\nNo debug log found.")
        print("AI Result:", json.dumps(result, indent=2)[:500])

except Exception as e:
    print(f"Error: {e}")
