from uuid import uuid4

from fastapi.testclient import TestClient

from app.domain.valueObjects.email import Email
from app.main import app, container

client = TestClient(app)
REGISTER_URL = "/api/v1/auth/register"


def _payload(email: str | None = None, **overrides: str) -> dict[str, str]:
    data = {
        "names": "Juan",
        "last_names": "Pérez",
        "email": email or f"hu01-{uuid4()}@example.com",
        "password": "Password123!",
    }
    data.update(overrides)
    return data


def test_register_endpoint_returns_201() -> None:
    payload = _payload()
    response = client.post(REGISTER_URL, json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["names"] == "Juan"
    assert body["last_names"] == "Pérez"
    assert body["email"] == payload["email"]
    assert "id" in body
    assert "password" not in body
    assert "password_hash" not in str(body)


def test_register_endpoint_duplicate_email_returns_409() -> None:
    payload = _payload()
    first = client.post(REGISTER_URL, json=payload)
    second = client.post(REGISTER_URL, json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "El correo electrónico ya está registrado"


def test_register_endpoint_invalid_email_returns_400() -> None:
    response = client.post(REGISTER_URL, json=_payload(email="no-es-un-correo"))
    assert response.status_code == 400


def test_register_endpoint_short_password_returns_400() -> None:
    response = client.post(REGISTER_URL, json=_payload(password="123"))
    assert response.status_code == 400


def test_register_endpoint_missing_names_returns_422() -> None:
    payload = _payload()
    payload["names"] = ""
    response = client.post(REGISTER_URL, json=payload)
    assert response.status_code == 422


def test_password_is_stored_as_bcrypt_hash() -> None:
    payload = _payload()
    response = client.post(REGISTER_URL, json=payload)
    assert response.status_code == 201

    stored = container.puerto_repositorio_agricultor.buscar_por_correo(Email(payload["email"]))
    assert stored is not None
    assert stored.hash_contrasena.value != payload["password"]
    assert stored.hash_contrasena.value.startswith("$2")
    assert payload["password"] not in stored.hash_contrasena.value
