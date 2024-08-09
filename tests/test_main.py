from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_startup():
    """
    Test to verify that the FastAPI application starts up successfully.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Tartarus API"
