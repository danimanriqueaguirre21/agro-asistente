from uuid import uuid4

import jwt
from fastapi.testclient import TestClient

from app.main import app, container

client = TestClient(app)
REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"


def _register(email: str | None = None, password: str = "Password123!") -> dict[str, str]:
    payload = {
        "names": "Juan",
        "last_names": "Pérez",
        "email": email or f"hu02-{uuid4()}@example.com",
        "password": password,
    }
    response = client.post(REGISTER_URL, json=payload)
    assert response.status_code == 201
    return payload


def test_login_endpoint_returns_200_and_bearer_token() -> None:
    payload = _register()
    response = client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["farmer"]["email"] == payload["email"]
    assert body["farmer"]["names"] == "Juan"
    assert "password" not in body
    assert "password_hash" not in str(body)
    assert "password" not in body["farmer"]


def test_login_unknown_user_returns_401() -> None:
    response = client.post(
        LOGIN_URL,
        json={"email": f"missing-{uuid4()}@example.com", "password": "Password123!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_login_wrong_password_returns_401() -> None:
    payload = _register()
    response = client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": "OtraClave123!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_login_missing_password_returns_422() -> None:
    response = client.post(LOGIN_URL, json={"email": "juan@example.com", "password": ""})
    assert response.status_code == 422


def test_login_jwt_is_signed_and_contains_required_claims() -> None:
    payload = _register()
    response = client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert response.status_code == 200
    body = response.json()
    farmer_id = body["farmer"]["id"]
    decoded = jwt.decode(
        body["access_token"],
        container.settings.jwt_secret,
        algorithms=[container.settings.jwt_algorithm],
    )
    assert decoded["sub"] == farmer_id
    assert decoded["email"] == payload["email"]
    assert "exp" in decoded
    assert "password" not in decoded
    assert "password_hash" not in decoded
