import sys
import os
import json
import re

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_editing import robust_replace

# Load the actual current_storyboard.txt content
with open('backend/current_storyboard.txt', 'r', encoding='utf-8') as f:
    current_doc = f.read()

# Simulate what the AI might provide (slightly simplified or formatted differently)
search_string = "• Definition of Generative AI: An introduction to Generative AI as a subset of artificial intelligence focused on creating data that imitates real-world information. • Historical Evolution: Delve into the foundation of Generative AI. • Applications of Generative AI: Gain insights into the diverse use cases."
replace_string = "Shortened version: Generative AI creates synthetic data. It started in the 90s and has many uses today."

print("Testing hyper-robust replacement with PRODUCTION CONTENT...")
print(f"Original doc length: {len(current_doc)}")

updated_doc = robust_replace(current_doc, search_string, replace_string)

if updated_doc != current_doc:
    print("\nSUCCESS: Document was modified even with a non-exact search string!")
    # Check if the replacement happened in the right place
    if replace_string in updated_doc:
        print("Replacement found in new document.")
else:
    print("\nFAIL: Document remained identical. Matching failed.")

# Test with multiline row
search_row = """| On-Screen Text (OST) | Audio Narration | Visual Instructions & Developer Notes |
| :-- | :-- | :-- |
| • Key milestones in the history of Generative AI<br>• Contributions of pioneering researchers in the field |"""
replace_row = "| NEW OST | NEW AUDIO | NEW VISUAL |"

print("\nTesting multiline row replacement...")
updated_doc_2 = robust_replace(current_doc, search_row, replace_row)
if updated_doc_2 != current_doc:
    print("SUCCESS: Multiline row replaced.")
else:
    print("FAIL: Multiline row replacement failed.")
