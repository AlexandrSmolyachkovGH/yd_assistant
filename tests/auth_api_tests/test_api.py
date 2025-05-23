from fastapi.testclient import TestClient

from yandex_auth.main import app

client = TestClient(app)


def test_server_status():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
