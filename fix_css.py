import os

path = 'instructional_ai_system/frontend_react/src/index.css'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

imports = []
themes = []
rest = []

in_theme = False
theme_block = []

for line in lines:
    stripped = line.strip()
    if stripped.startswith('@import'):
        imports.append(line)
        continue
    
    if stripped.startswith('@theme'):
        in_theme = True
        theme_block.append(line)
        if '}' in stripped:
            in_theme = False
            themes.append("".join(theme_block))
            theme_block = []
        continue
    
    if in_theme:
        theme_block.append(line)
        if '}' in stripped:
            in_theme = False
            themes.append("".join(theme_block))
            theme_block = []
        continue
    
    rest.append(line)

# De-duplicate imports
seen_imports = set()
unique_imports = []
for imp in imports:
    if imp.strip() not in seen_imports:
        unique_imports.append(imp)
        seen_imports.add(imp.strip())

new_content = "".join(unique_imports) + "\n" + "".join(themes) + "\n" + "".join(rest)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Fixed {path}. Combined {len(unique_imports)} imports and {len(themes)} themes at the top.")
for i, imp in enumerate(unique_imports):
    print(f"Import {i+1}: {imp.strip()}")
