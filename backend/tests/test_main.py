from fastapi.testclient import TestClient
from main import app

# Create a test client for our FastAPI app
client = TestClient(app)


def test_read_root():
    """
    Test that the root endpoint ("/") is reachable and returns a
    successful (200 OK) response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Hello": "Stealth Seekers Foresight Engine is Online"
    }
