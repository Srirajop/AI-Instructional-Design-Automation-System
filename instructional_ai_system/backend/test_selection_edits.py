import sys
import os
import json

# Add backend to path to import ai_editing
sys.path.append(os.path.join(os.getcwd(), 'instructional_ai_system', 'backend'))

from app.services.ai_editing import ai_edit_document

# Mock API Key
api_key = os.environ.get("GROQ_API_KEY")

def test_selection_edit(doc_content, doc_type, selection):
    print(f"\n--- Testing Selection Edit for {doc_type} ---")
    print(f"Selection: {selection['text']} at {selection['screen_num']}, Col: {selection['col_index']}")
    
    result = ai_edit_document(
        api_key=api_key,
        current_doc=doc_content,
        user_instruction=f"rewrite the selected text to be more engaging",
        doc_type=doc_type,
        selected_text=selection['text'],
        selected_screen_num=selection['screen_num'],
        selected_col_index=selection['col_index']
    )
    
    print(f"Assistant Reply: {result['assistant_reply']}")
    print(f"Is Edit: {result['is_edit']}")
    if result['is_edit']:
        for d in result['diff']:
            print(f"  Changed {d['screen_num']} | {d['col_name']}: '{d['old_content']}' -> '{d['new_content']}'")
    return result

# 1. Storyboard Type 1
sb1 = """Module 1: Intro
Screen 1.1 Title
| OST | Audio | Visual |
|---|---|---|
| Welcome to the course. | Hello everyone. | Shot of a desk. |
"""
test_selection_edit(sb1, "Storyboard", {"text": "Welcome to the course.", "screen_num": "1.1", "col_index": 0})

# 2. Storyboard Type 2
sb2 = """Module 1: Intro
| Section | Topics | Visuals | OST | Audio | Status | Actions |
|---|---|---|---|---|---|---|
| Intro | Welcome | desk | Hi | Listen | done | none |
"""
test_selection_edit(sb2, "Storyboard Type 2", {"text": "Welcome", "screen_num": "Intro", "col_index": 1})

# 3. Design Document
dd = """# Design Document
| Module | Delivery | Objectives | Topics | Strategy | Activities | Duration |
|---|---|---|---|---|---|---|
| Module 1 | Online | Learn AI | ML Basics | Video | Quiz | 10m |
"""
test_selection_edit(dd, "Design Document", {"text": "ML Basics", "screen_num": "Module 1", "col_index": 3})
