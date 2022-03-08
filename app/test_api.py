from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/users")
    assert response.status_code == 200
    # assert response.json() == {'status': 'ok'}