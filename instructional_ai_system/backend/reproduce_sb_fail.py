import requests
import json

def test_generate():
    url = "http://localhost:8000/api/storyboard/d8020/generate?storyboard_type=Type 1"
    headers = {
        "Accept": "text/event-stream",
        "Authorization": "Bearer fake_token" # We'll see if it gets past auth
    }
    
    try:
        # We'll use a real token if we can, but let's see if the server even responds
        response = requests.post(url, headers=headers, stream=True)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        for line in response.iter_lines():
            if line:
                print(f"Data: {line.decode('utf-8')}")
                break # Just see first event
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_generate()
