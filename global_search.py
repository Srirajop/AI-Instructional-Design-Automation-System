import os

search_str = "Geist"
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.css') or file.endswith('.jsx') or file.endswith('.js'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if search_str in line:
                            print(f"{path}:{i}: {line.strip()}")
            except:
                pass
