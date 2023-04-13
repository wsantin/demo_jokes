from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

def test_jock_random():
    response = client.get("/v1/jokes/random")
    assert response.status_code == 200

def test_test_read_jocke():
    response = client.get("/v1/jokes/1")
    assert response.status_code == 200

def test_increment():
    response = client.get("/v1/others/increment?number=5")
    assert response.status_code == 200

def test_increment_incorrect():
    response = client.get("/v1/others/increment?number=a")
    assert response.status_code == 422