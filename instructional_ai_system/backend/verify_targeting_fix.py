import re

def test_logic(user_instruction, chat_history):
    # Simplified version of the logic in ai_editing.py
    python_hint = None
    curr_match = re.search(r'Screen\s+(\d+\.\d+)', user_instruction, re.IGNORECASE)
    if curr_match:
        python_hint = f"Screen {curr_match.group(1)}"
    elif chat_history:
        for msg in reversed(chat_history):
            match = re.search(r'Screen\s+(\d+\.\d+)', msg['content'], re.IGNORECASE)
            if match:
                python_hint = f"Screen {match.group(1)}"
                break
    return python_hint

# Test 1: Explicit screen in current instruction (should override history)
instr1 = "Please change Screen 1.8 ost"
hist1 = [{"role": "assistant", "content": "I updated Screen 1.4"}]
res1 = test_logic(instr1, hist1)
print(f"Test 1 (Explicit): '{instr1}' with History 1.4 -> Result: {res1}")
assert res1 == "Screen 1.8"

# Test 2: Pronoun in current instruction (should use history)
instr2 = "change its visuals"
hist2 = [{"role": "assistant", "content": "I updated Screen 1.4"}]
res2 = test_logic(instr2, hist2)
print(f"Test 2 (History): '{instr2}' with History 1.4 -> Result: {res2}")
assert res2 == "Screen 1.4"

# Test 3: Multiple screens in history
instr3 = "edit that one"
hist3 = [
    {"role": "user", "content": "Screen 1.1 stuff"},
    {"role": "assistant", "content": "I updated Screen 1.1"},
    {"role": "user", "content": "now Screen 2.2"},
    {"role": "assistant", "content": "OK Screen 2.2 updated"}
]
res3 = test_logic(instr3, hist3)
print(f"Test 3 (Multi History): '{instr3}' with History 2.2 -> Result: {res3}")
assert res3 == "Screen 2.2"

print("ALL TESTS PASSED")
