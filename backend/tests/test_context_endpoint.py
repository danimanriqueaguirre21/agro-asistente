from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from fastapi.testclient import TestClient

from app.main import app, container

client = TestClient(app)
REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
CONTEXTS_URL = "/api/v1/contexts"


def _register_and_login(email: str | None = None) -> dict[str, str]:
    payload = {
        "names": "Ana",
        "last_names": "Huaman",
        "email": email or f"hu03-{uuid4()}@example.com",
        "password": "Password123!",
    }
    register = client.post(REGISTER_URL, json=payload)
    assert register.status_code == 201
    login = client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login.status_code == 200
    return {
        "email": payload["email"],
        "token": login.json()["access_token"],
        "farmer_id": login.json()["farmer"]["id"],
    }


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _context_payload(**overrides: str) -> dict[str, str]:
    data = {
        "plot_name": "Parcela 1",
        "crop": "papa",
        "region": "Huancayo",
        "notes": "Campana seca",
    }
    data.update(overrides)
    return data


def test_create_context_requires_auth() -> None:
    response = client.post(CONTEXTS_URL, json=_context_payload())
    assert response.status_code == 401
    listed = client.get(CONTEXTS_URL)
    assert listed.status_code == 401


def test_create_context_rejects_invalid_token() -> None:
    response = client.post(
        CONTEXTS_URL,
        json=_context_payload(),
        headers=_auth("token-invalido"),
    )
    assert response.status_code == 401


def test_create_context_rejects_expired_token() -> None:
    user = _register_and_login()
    expired = jwt.encode(
        {
            "sub": user["farmer_id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        container.settings.jwt_secret,
        algorithm=container.settings.jwt_algorithm,
    )
    response = client.post(
        CONTEXTS_URL,
        json=_context_payload(),
        headers=_auth(expired),
    )
    assert response.status_code == 401


def test_create_and_list_context_for_authenticated_farmer() -> None:
    user = _register_and_login()
    created = client.post(
        CONTEXTS_URL,
        json=_context_payload(),
        headers=_auth(user["token"]),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["crop"] == "papa"
    assert body["farmer_id"] == user["farmer_id"]
    assert body["is_selected"] is False

    listed = client.get(CONTEXTS_URL, headers=_auth(user["token"]))
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["id"] == body["id"]


def test_create_context_ignores_forged_farmer_id() -> None:
    user = _register_and_login()
    other_id = str(uuid4())
    response = client.post(
        CONTEXTS_URL,
        json={**_context_payload(), "farmer_id": other_id},
        headers=_auth(user["token"]),
    )
    assert response.status_code == 201
    assert response.json()["farmer_id"] == user["farmer_id"]
    assert response.json()["farmer_id"] != other_id


def test_create_context_invalid_payload_returns_422() -> None:
    user = _register_and_login()
    response = client.post(
        CONTEXTS_URL,
        json={"plot_name": "X", "crop": "", "region": "Huancayo"},
        headers=_auth(user["token"]),
    )
    assert response.status_code == 422


def test_select_own_context() -> None:
    user = _register_and_login()
    created = client.post(
        CONTEXTS_URL,
        json=_context_payload(),
        headers=_auth(user["token"]),
    )
    context_id = created.json()["id"]
    selected = client.post(
        f"{CONTEXTS_URL}/{context_id}/select",
        headers=_auth(user["token"]),
    )
    assert selected.status_code == 200
    assert selected.json()["is_selected"] is True


def test_farmers_cannot_see_or_select_each_others_contexts() -> None:
    farmer_a = _register_and_login()
    farmer_b = _register_and_login()
    context_a = client.post(
        CONTEXTS_URL,
        json=_context_payload(crop="papa"),
        headers=_auth(farmer_a["token"]),
    ).json()
    context_b = client.post(
        CONTEXTS_URL,
        json=_context_payload(crop="maiz"),
        headers=_auth(farmer_b["token"]),
    ).json()

    list_a = client.get(CONTEXTS_URL, headers=_auth(farmer_a["token"])).json()
    list_b = client.get(CONTEXTS_URL, headers=_auth(farmer_b["token"])).json()
    assert [item["id"] for item in list_a] == [context_a["id"]]
    assert [item["id"] for item in list_b] == [context_b["id"]]

    select_b_as_a = client.post(
        f"{CONTEXTS_URL}/{context_b['id']}/select",
        headers=_auth(farmer_a["token"]),
    )
    select_a_as_b = client.post(
        f"{CONTEXTS_URL}/{context_a['id']}/select",
        headers=_auth(farmer_b["token"]),
    )
    assert select_b_as_a.status_code == 404
    assert select_a_as_b.status_code == 404
