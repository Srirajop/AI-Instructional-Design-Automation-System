with open('instructional_ai_system/frontend_react/src/index.css', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if '@import' in line:
            print(f"{i}: {line.strip()}")
        if '@theme' in line:
            print(f"{i}: {line.strip()}")
