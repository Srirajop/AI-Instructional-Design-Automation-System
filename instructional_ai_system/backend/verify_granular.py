import sys
import os
import re

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_editing import structural_replace_granular

# Sample doc with long content
doc = """
Screen 1.1 Title: Intro to AI

| ON-SCREEN TEXT (OST) | AUDIO | VISUAL |
| :-- | :-- | :-- |
| This is a very long sentence about artificial intelligence that needs to be shortened significantly for easier reading. | AUDIO | VISUAL |
"""

print("Testing structural_replace_granular...")
# Simulate AI trying to replace JUST the long sentence
# search_snippet is the "old" text
search_snippet = "This is a very long sentence about artificial intelligence that needs to be shortened significantly for easier reading."
replace_str = "AI is complex but beneficial."

new_doc = structural_replace_granular(doc, "1.1", "ost", search_snippet, replace_str)

if "AI is complex but beneficial." in new_doc:
    print("SUCCESS: Content replaced.")
    # Check if it's still a table
    if "| AI is complex but beneficial. | AUDIO | VISUAL |" in new_doc:
        print("SUCCESS: Row structure preserved.")
else:
    print("FAIL: Content not found.")
    print("Output:", new_doc)
