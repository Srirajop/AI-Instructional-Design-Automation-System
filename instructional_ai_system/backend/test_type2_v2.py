import os
import json
from app.services.ai_editing import ai_edit_document
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

storyboard_type2 = """
# STORYBOARD - AI and ML Fundamentals

MODULE 1: Introduction to AI

| Section | Topics | Visual Instructions/Developer Notes | On-screen text | Audio Narration | Status | Actions required |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Intro | What is AI? | • Simple static image | • AI Basics<br>• Definitions | This screen introduces the basic concepts of AI. | Draft | None |
| History | AI History | • Timeline graphic | • 1950s: Turing Test<br>• 1990s: IBM Deep Blue | We will look at the key milestones in AI history. | Draft | Fix bullets |
"""

results = []

def test_edit(msg):
    print(f"Testing: {msg}")
    result = ai_edit_document(api_key, storyboard_type2, msg, doc_type="Storyboard Type 2", chat_history=[])
    simplified = {
        "request": msg,
        "reply": result['assistant_reply'],
        "is_edit": result['is_edit'],
        "diff_count": len(result.get('diff', []))
    }
    if result['is_edit']:
        simplified["edits"] = [
            {"target": d['screen_num'], "col": d['col_name'], "old": d['old_content'], "new": d['new_content']}
            for d in result['diff']
        ]
    results.append(simplified)

if __name__ == "__main__":
    test_edit("update the on-screen text for the Intro section to include 'Artificial Intelligence'")
    test_edit("make the audio narration for the History section more exciting")
    with open("test_results_type2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Results saved to test_results_type2.json")
