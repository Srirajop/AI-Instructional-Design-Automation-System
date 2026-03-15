import sys
import os
import json

# Add backend to path to import ai_editing
sys.path.append(os.path.join(os.getcwd(), 'instructional_ai_system', 'backend'))

from app.services.ai_editing import ai_edit_document

# Mock API Key
api_key = os.environ.get("GROQ_API_KEY")

def test_precision_edit(doc_content, doc_type, selection):
    print(f"\n--- Testing Precision Edit for {doc_type} ---")
    print(f"Targeting: {selection['screen_num']} (Col {selection['col_index']})")
    
    result = ai_edit_document(
        api_key=api_key,
        current_doc=doc_content,
        user_instruction=f"update the topics for the selected row to mentioned artificial intelligence",
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

# Document with duplicate "Intro" rows in Module 1 and Module 2
duplicate_doc = """# Course Design
Module 1: Logistics
| Module | Delivery | Objectives | Topics | Strategy | Activities | Duration |
|---|---|---|---|---|---|---|
| Intro | Online | Learn Basic | Logistics | Video | None | 5m |

Module 2: Technology
| Module | Delivery | Objectives | Topics | Strategy | Activities | Duration |
|---|---|---|---|---|---|---|
| Intro | Online | Learn Tech | Cloud | Video | Lab | 10m |
"""

# Test targeting Module 2's Intro (without combined ID it might hit Module 1)
print("\n[SCENARIO: TARGETING MODULE 2's INTRO]")
test_precision_edit(duplicate_doc, "Design Document", {
    "text": "Cloud", 
    "screen_num": "Module 2 | Intro", 
    "col_index": 3
})
