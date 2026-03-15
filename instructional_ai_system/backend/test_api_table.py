import requests, json
prompt = """USER REQUEST: "Update Screen 1.3 narration to be more creative"

Please perform the transformation requested above on the following document.
Ensure pipes/dividers are preserved exactly. Respond ONLY with JSON to match the Schema from the System Prompt.

<current_document>
| Screen | Text | Narration |
|---|---|---|
| 1.1 | Welcome | Hello |
| 1.2 | Overview | This is an overview |
| 1.3 | Details | These are the details |
| 1.4 | Summary | Goodbye |
</current_document>

You are a High-Precision Instructional Design Architect.
You must help the user with their Storyboard through high-fidelity transformations.

**STRICT TRACK CHANGES (WORD-STYLE) MODE**:
1. **TRANSFORM**: When asked for an edit, RE-WRITE and REPLACE the existing text.
2. **FULL DOCUMENT (CRITICAL)**: You must ALWAYS return the ENTIRE, COMPLETE document state in the `updated_document` field. DO NOT output partial snippets.

**IS_EDIT FLAG (CRITICAL)**:
1. Set `"is_edit": true` ONLY if you have performed a document transformation.

**SCHEMA**:
{
  "assistant_reply": "Summary of your changes or your conversational response.",
  "updated_document": "The FULL AND COMPLETE Storyboard text with your edits applied. Do not output anything else here.",
  "is_edit": true
}
"""
res = requests.post('https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQnBtS2ptdFNtblZXcldCVV80M2ZLbElhOHhGMzd1Z1c1NWpiMXdfMU5uX3VVWkR5Q0N3OGEwUElfNWRIWVI3QkFxQ2FCU2ZRV0JLSVBja2dBaXR6dTN2WktVZVE9PQ==', json={'prompt': prompt})
print(res.text)
