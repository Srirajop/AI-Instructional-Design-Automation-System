import os
import sys
from dotenv import load_dotenv

# Load env vars for API keys
load_dotenv()

# Add project root to path
sys.path.append(os.getcwd())

from app.services import ai_editing

# Mock data
current_doc = """
**Screen 1.3 Title: Generative AI vs. Other AI Types**
| On-Screen Text (OST) | Audio Narration | Visual Instructions & Developer Notes |
| :--- | :--- | :--- |
| • Comparison of Generative AI with other AI types<br>• Key differences and similarities | Generative AI is a type of artificial intelligence that is distinct from other AI types. While all AI systems are designed to perform specific tasks. | Visual description: A diagram comparing Generative AI with other AI types appears on the screen. |
"""

def test_targeting(instruction, expected_col):
    print(f"\nTesting: {instruction}")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in environment.")
        return

    # Using a small subset of history
    chat_history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

    try:
        result = ai_editing.ai_edit_document(
            api_key=api_key,
            current_doc=current_doc,
            user_instruction=instruction,
            doc_type="Storyboard",
            chat_history=chat_history
        )
        
        print(f"Assistant Reply: {result.get('assistant_reply')}")
        if result.get("is_edit"):
            for i, edit in enumerate(result.get("edits", [])):
                search = edit.get("search_string", "")
                replace = edit.get("replace_string", "")
                print(f"Edit {i+1} Search: {search[:100]}...")
                
                # Check if it targeted the right column
                if expected_col == "OST":
                    if "Comparison of Generative AI with other AI types" in search:
                        print("SUCCESS: Targeted OST column.")
                    else:
                        print("FAILURE: Did not target OST column.")
                elif expected_col == "Audio":
                    if "Generative AI is a type of artificial intelligence" in search:
                        print("SUCCESS: Targeted Audio column.")
                    else:
                        print("FAILURE: Did not target Audio column.")
                elif expected_col == "Visuals":
                    if "Visual description: A diagram comparing Generative AI" in search:
                        print("SUCCESS: Targeted Visuals column.")
                    else:
                        print("FAILURE: Did not target Visuals column.")
        else:
            print("No edit returned.")
            
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    # Test 1: Explicit OST request
    test_targeting("change screen 1.3 ost to be more descriptive", "OST")
    
    # Test 2: Explicit Audio request
    # test_targeting("change the audio for screen 1.3 to include a friendly welcome", "Audio")
