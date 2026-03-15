import requests
import json

prompt = """
You are a High-Precision Instructional Design Architect.

**STRICT TRACK CHANGES (WORD-STYLE) MODE**:
1. **TRANSFORM**: When asked for an edit, RE-WRITE and REPLACE the existing text.
2. **FULL DOCUMENT**: Always return the ENTIRE current document state in `updated_document`.
3. **JSON FORMAT**: You must return ONLY a valid JSON object.

**IS_EDIT FLAG (CRITICAL)**:
1. Set `"is_edit": true` ONLY if you have performed a document transformation or updated any text within the document.

**SCHEMA**:
{
  "assistant_reply": "Summary of your changes or your conversational response.",
  "updated_document": "The complete current document state (with edits applied if requested, else unchanged).",
  "is_edit": true
}

USER REQUEST: "Change the title to WOW"
Please perform the transformation requested above on the following document.
Ensure pipes/dividers are preserved exactly. Respond ONLY with JSON to match the Schema from the System Prompt.

<current_document>
# Old Title
Some text.
</current_document>
"""

api_url = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQnBtS2ptdFNtblZXcldCVV80M2ZLbElhOHhGMzd1Z1c1NWpiMXdfMU5uX3VVWkR5Q0N3OGEwUElfNWRIWVI3QkFxQ2FCU2ZRV0JLSVBja2dBaXR6dTN2WktVZVE9PQ=="

res = requests.post(
    api_url,
    json={"prompt": prompt},
    headers={"Content-Type": "application/json"}
)

print(res.text)
