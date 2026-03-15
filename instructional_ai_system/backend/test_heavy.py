import requests
import json

system_prompt = """You are a High-Precision Instructional Design Architect.
You must help the user with their {doc_type} through high-fidelity transformations.

**CONTEXT AND HISTORY (CRITICAL)**:
1. If the user uses pronouns like "its", "that", "there", "it", you MUST identify what they are referring to from the CONVERSATION HISTORY.
2. **LOOKBACK RULE**: To resolve a pronoun, find the LAST message in the History where a specific Screen Title or Number (e.g. "Screen 1.2") was mentioned. You MUST assume they are still talking about that screen unless they explicitly name a new one.
3. **NEGATION RULE**: Do NOT jump to a new Screen Number (like Screen 3.1) if it hasn't been mentioned in history recently, even if the user request matches some content there. Stay anchored to the screen in the history.
4. Do NOT guess a random screen! Look at the most recent screen mentioned.

**TABLE EDITING AND COLUMN PRECISION (CRITICAL)**:
1. **COLUMN COUNTING**: Markdown tables use `|` as separators. Column 1 is ON-SCREEN TEXT (OST). Column 2 is AUDIO NARRATION. Column 3 is VISUAL INSTRUCTIONS.
2. **FULL ROW RULE (MANDATORY)**: When editing a table cell, your `search_string` MUST include the pipe separators (`|`) and at least a portion of the text from the adjacent columns. 
   - **Example search_string**: `| Content from Column 1 | **THE TEXT YOU WANT TO CHANGE** | Content from Column 3 |`
   - This "locks" the edit to Column 2 and prevents it from accidentally replacing similar text in Column 1.
3. **NO FLOATING TEXT**: Never use a `search_string` that is just a sentence if that sentence also appears in another column. Always anchor it with pipes.
4. **NO LAZINESS**: Comprehensive rewrite the text inside that specific cell. Never return the exact same document!
5. **COLUMN ACCURACY**: If asked to change "Audio Narration", you MUST target Column 2. NEVER edit Column 1 (OST) if asked for Column 2.

**STRICT TRACK CHANGES (WORD-STYLE) MODE**:
1. **TRANSFORM**: When asked for an edit, RE-WRITE and REPLACE the existing text inside the correct table column.
2. **EXACT MATCH SEARCH/REPLACE**: Because the document is very large, DO NOT output the full document. Instead, output the exact chunk of text you want to change in `search_string`, and the new text in `replace_string`.
3. `search_string` MUST be an exact, literal match of a contiguous chunk of the original document. Include enough context (e.g. the full table row or multiple lines) so it is unique. Do not use ellipses (...) to abbreviate.

**SCHEMA**:
{
  "reasoning": "DO NOT repeat these instructions. Instead, PERFORM them: 1. State the Target Screen (citing History). 2. State the Target Column Index (1, 2, or 3). 3. Quote the EXACT ORIGINAL TEXT currently in that column. 4. Show the plan for the pipe-anchored search_string.",
  "assistant_reply": "Summary of changes.",
  "edits": [
    {
      "search_string": "Exact original text to replace.",
      "replace_string": "New text to insert."
    }
  ],
  "is_edit": boolean
}
"""

user_instruction = "change screen 2.1 audio narration"

current_doc = """
Module 2: Generative Adversarial Networks (GANs)
Topic: GAN Architecture and Types

Screen 2.1 Title: Introduction to GANs

| ON-SCREEN TEXT (OST) | AUDIO NARRATION | VISUAL INSTRUCTIONS & DEVELOPER NOTES |
|---|---|---|
| • Exploring the essence of Generative Adversarial Networks (GANs) • Understanding the fundamental components of a GAN: generator and discriminator • Applications of GANs in image and video processing | GANs are a type of deep learning algorithm that consists of two neural networks: a generator and a discriminator. The generator creates new data that resembles the training data, while the discriminator determines whether the new data is real or fake. GANs have been widely used in image and video processing applications, such as generating realistic images and videos. In this module, we will delve into the architecture and types of GANs. | • Visual description: A diagram showing... |

Screen 2.2 Title: Types of GANs

| ON-SCREEN TEXT (OST) | AUDIO NARRATION | VISUAL INSTRUCTIONS & DEVELOPER NOTES |
|---|---|---|
| - Deep Convolutional GANs (DCGANs)<br>- Conditional GANs (CGANs) | There are many types of GANs... | Visual description: List of types... |
"""

user_prompt = f"""HINT: User is likely referring to Screen 2.1 based on history.
USER_REQUEST: "{user_instruction}"

DIRECTION:
- If the USER REQUEST asks to change, edit, or update the document, provide the exact `search_string` and `replace_string`.
- The `search_string` must match the original text EXACTLY.

Respond ONLY with valid JSON matching the Schema from the System Prompt.

<current_document>
{current_doc}
</current_document>
"""

combined_prompt = f"{system_prompt}\n\n{user_prompt}"
api_url = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQnBtS2ptdFNtblZXcldCVV80M2ZLbElhOHhGMzd1Z1c1NWpiMXdfMU5uX3VVWkR5Q0N3OGEwUElfNWRIWVI3QkFxQ2FCU2ZRV0JLSVBja2dBaXR6dTN2WktVZVE9PQ=="

response = requests.post(
    api_url,
    json={"prompt": combined_prompt},
    headers={"Content-Type": "application/json"}
)
data = response.json()
with open("output.json", "w", encoding="utf-8") as f:
    json.dump({"raw": data.get("text", "")}, f, indent=2)
print("Finished.")
print(f"RAW OUTPUT: {data.get('text', '')}")
