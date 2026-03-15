import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'http://localhost:8000/api/auth/register',
    data=json.dumps({'name':'test','email':'test3@test.com','password':'test'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Exception: {e}")
