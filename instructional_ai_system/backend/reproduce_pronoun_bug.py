import sys
sys.path.append('d:/Downloads/StoryBoardAI/instructional_ai_system/backend')
from app.services import ai_editing
import os
import json

api_key = os.getenv("GROQ_API_KEY")

# Mock chat history matching the database state
history = [
    {"role": "user", "content": "please change ost of screen 1.4 to more descriptive"},
    {"role": "assistant", "content": "I will update the On-Screen Text for Screen 1.4 to be more descriptive as requested."},
    {"role": "user", "content": "change its visual instructions too"},
    {"role": "assistant", "content": "I will update the Visual Instructions for Screen 1.4 to be more descriptive as requested."},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hi there! How can I assist you with the Instructional Design Document today? Do you want to review the 'Audio Narration' section or make any updates?"},
    {"role": "user", "content": "please change screen 2.2 ost"},
    {"role": "assistant", "content": "I will update the on-screen text for Screen 2.2 as requested."}
]

user_instruction = "please change its visual instructions"
doc_type = "Storyboard"
current_doc = """
**Screen 1.1 Title:** What is Generative AI?
| OST | Audio | Visuals |
|---|---|---|
| ... | ... | ... |

**Screen 1.4 Title:** Key Benefits and Challenges of Generative AI
| OST | Audio | Visuals |
|---|---|---|
| • Enhancing ... | Generative AI ... | • Visual description: An innovative 3D visualization ... |

**Screen 2.2 Title:** Types of GANs
| OST | Audio | Visuals |
|---|---|---|
| • Diving ... | DCGAN is a type ... | • Create a table to compare ... |
"""

print("Running reproduction test...")
response = ai_editing.ai_edit_document(api_key, current_doc, user_instruction, doc_type, history)

print("\nAI RESPONSE:")
print(f"Assistant Reply: {response.get('assistant_reply')}")
print(f"Is Edit: {response.get('is_edit')}")
if response.get('is_edit'):
    for i, edit in enumerate(response.get('edits', [])):
        print(f"Edit {i+1} Search: {edit.get('search_string')[:100]}...")
