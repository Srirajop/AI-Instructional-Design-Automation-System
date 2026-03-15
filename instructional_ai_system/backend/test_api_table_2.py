import json
import difflib
from app.services.ai_editing import extract_json

print('Extracting AI JSON to see if changes are preserved')
raw = open('test_api_table.py').read()
# Note: we need to run test again and get exact payload 
