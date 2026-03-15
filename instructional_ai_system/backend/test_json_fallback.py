import sys
import os

# Add the backend directory to sys.path so we can import app
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_editing import extract_json

def test_extract_json_resilience():
    print("Testing extract_json resilience...")
    
    # 1. Valid JSON
    valid_json = '{"reasoning": "test", "assistant_reply": "hello", "edits": [], "is_edit": false}'
    result = extract_json(valid_json)
    assert result["assistant_reply"] == "hello"
    print("✓ Valid JSON passed")
    
    # 2. JSON with surrounding text
    wrapped_json = 'Here is the result: {"reasoning": "test", "assistant_reply": "wrapped", "edits": [], "is_edit": false} Hope this helps!'
    result = extract_json(wrapped_json)
    assert result["assistant_reply"] == "wrapped"
    print("✓ Wrapped JSON passed")
    
    # 3. Malformed but repairable JSON
    malformed_json = '{"reasoning": "test", "assistant_reply": "broken", "edits": [], "is_edit": false'
    result = extract_json(malformed_json)
    assert result["assistant_reply"] == "broken"
    print("✓ Malformed/Repairable JSON passed")
    
    # 4. Pure natural language (should hit our new fallback)
    raw_text = "I see you want to shorten the on-screen text of Screen 1.1. How would you like to modify it?"
    result = extract_json(raw_text)
    assert result["assistant_reply"] == raw_text
    assert result["is_edit"] == False
    assert result["reasoning"] == "Fallback due to JSON extraction failure."
    print("✓ Fallback for natural language passed")

if __name__ == "__main__":
    try:
        test_extract_json_resilience()
        print("\nALL EXTRACTION TESTS PASSED!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
