from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.post(
    "/api/auth/register",
    json={"name": "test", "email": "test5@test.com", "password": "test"}
)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
