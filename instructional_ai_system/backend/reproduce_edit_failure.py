from app.services.ai_editing import ai_edit_document, parse_document_into_sections

def test_matching_failure():
    # Sample document with bullets in row label
    doc = """
### MODULE 1: Intro
| Section | Topics | Visuals | OST | Audio | Status | Actions |
|---|---|---|---|---|---|---|
| Screen 1.1 | • Intro to GANs<br>• Basics | View | Hello | Welcome | Draft | None |

Screen 2.5 Title: Summary
| Section | Topics | Visuals | OST | Audio | Status | Actions |
|---|---|---|---|---|---|---|
| • Summary of key points<br>• Final thoughts | GAN Summary | Image | Text | Audio content here. | Draft | None |
"""
    
    # CASE 1: Truncated Label
    # Full label: "• Summary of key points<br>• Final thoughts"
    # AI returns: "• Summary of key points • Final thoughts" (truncated/cleaned)
    target_id_truncated = "Screen 2.5 | • Summary of key points • Final thoughts" 
    print(f"\nTEST CASE 1: Truncated Label matching")
    result1 = ai_edit_document(
        api_key="fake_key",
        current_doc=doc,
        user_instruction="Make it descriptive",
        doc_type="Storyboard Type 2",
        selected_text="Audio content here.",
        selected_screen_num=target_id_truncated,
        selected_col_index=4 
    )
    print(f"Result 1: {result1.get('is_edit')}")
    if result1.get('is_edit'): print("✅ Truncated label matched.")
    else: print(f"❌ Truncated label failed. Reply: {result1.get('assistant_reply')}")

    # CASE 2: High col_index safety
    # Type 1 Doc has only 3 cols. AI targets col 4.
    doc_type1 = """
Screen 1.1 Title: Intro
| OST | Audio | Visual |
|---|---|---|
| Text | Audio | Visual |
"""
    print(f"\nTEST CASE 2: Index Safety (Type 1 doc, AI targets col 4)")
    result2 = ai_edit_document(
        api_key="fake_key",
        current_doc=doc_type1,
        user_instruction="Change audio",
        doc_type="Storyboard Type 2", # AI thinks it's Type 2
        selected_text="Audio",
        selected_screen_num="Screen 1.1",
        selected_col_index=4 # AI uses Type 2 index for audio
    )
    print(f"Result 2: {result2.get('is_edit')}")
    if result2.get('is_edit'):
        print("✅ Index safety applied (clamped to 2).")
        # Check if the last col (Visual) was updated instead of failing
        if "| Text | Audio |  Change audio  |" in result2.get('updated_document', ''):
             print("✅ Content applied to last available column.")
    else: print(f"❌ Index safety failed. Reply: {result2.get('assistant_reply')}")

if __name__ == "__main__":
    test_matching_failure()
