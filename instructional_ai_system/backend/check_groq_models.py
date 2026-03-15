from dotenv import load_dotenv; import os, requests, json; load_dotenv()
res = requests.get('https://api.groq.com/openai/v1/models', headers={'Authorization': 'Bearer ' + os.environ.get('GROQ_API_KEY')}).json()
print(json.dumps([m['id'] for m in res.get('data', [])], indent=2))
