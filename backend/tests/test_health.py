from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["service"] == "agro-asistente"
    assert payload["phase"] == "1"
    assert payload["architecture"] == "hexagonal"
    assert payload["mysql"] in {"connected", "disconnected"}
