search_str = "Geist"
with open('instructional_ai_system/frontend_react/src/index.css', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if search_str in line:
            print(f"{i}: {line.strip()}")
