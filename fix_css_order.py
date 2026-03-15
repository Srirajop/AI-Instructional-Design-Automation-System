import os

path = 'instructional_ai_system/frontend_react/src/index.css'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
imports = []
rest = []

for line in lines:
    if line.strip().startswith('@import'):
        imports.append(line)
    else:
        rest.append(line)

# Sort imports: fonts first, then tailwind, then others
fonts = [i for i in imports if 'fonts.googleapis.com' in i]
tailwind = [i for i in imports if 'tailwindcss' in i]
others = [i for i in imports if i not in fonts and i not in tailwind]

final_imports = fonts + tailwind + others
new_content = "".join(final_imports) + "".join(rest)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Reordered imports in {path}")
for i, line in enumerate(final_imports):
    print(f"{i+1}: {line.strip()}")
