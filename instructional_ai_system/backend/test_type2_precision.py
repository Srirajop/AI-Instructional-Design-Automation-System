import sys
import os
import json

# Add backend to path to import ai_editing
sys.path.append(os.path.join(os.getcwd(), 'instructional_ai_system', 'backend'))

from app.services.ai_editing import ai_edit_document

# Mock API Key
api_key = os.environ.get("GROQ_API_KEY")

def test_type2_precision(doc_content, selection):
    print(f"\n--- Testing Storyboard Type 2 Precision ---")
    print(f"Targeting: {selection['screen_num']} (Col {selection['col_index']})")
    
    result = ai_edit_document(
        api_key=api_key,
        current_doc=doc_content,
        user_instruction=f"make the audio narration for the History section more exciting and mention ancient Rome",
        doc_type="Storyboard Type 2",
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

# Storyboard Type 2 with 7 columns
type2_doc = """# Storyboard (Advanced)

Module 1: World History
| Section | Topics | Visuals | OST | Audio | Status | Actions |
|---|---|---|---|---|---|---|
| Intro | Welcome | Graphic of globe | Welcome back! | Hello and welcome to history. | Draft | None |
| History | Past Events | Timeline of dates | Dates and Facts | Let's look at the history of the world. | Draft | None |
| Quiz | Testing | Question mark | Are you ready? | Time for a quick quiz! | Ready | Review |
"""

# Scenario 1: Natural Language targeting "History" section Audio (Col 4)
print("\n[SCENARIO: NATURAL LANGUAGE EDIT FOR TYPE 2]")
test_type2_precision(type2_doc, {
    "text": None,
    "screen_num": None,
    "col_index": None
})

# Scenario 2: Selection-based targeting "History" section Visuals (Col 2)
print("\n[SCENARIO: SELECTION-BASED EDIT FOR TYPE 2]")
test_type2_precision(type2_doc, {
    "text": "Timeline of dates", 
    "screen_num": "Module 1: World History | History", 
    "col_index": 2
})
