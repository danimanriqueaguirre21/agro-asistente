from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.infrastructure.adapters.output.mysql.connection import create_mysql_engine
from app.main import app, container

client = TestClient(app)
REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
INGEST_URL = "/api/v1/knowledge/ingest"
DOCUMENTS_URL = "/api/v1/knowledge/documents"


def _register_and_login() -> dict[str, str]:
    payload = {
        "names": "Rosa",
        "last_names": "Quispe",
        "email": f"hu05-{uuid4()}@example.com",
        "password": "Password123!",
    }
    register = client.post(REGISTER_URL, json=payload)
    assert register.status_code == 201
    login = client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login.status_code == 200
    return {"token": login.json()["access_token"]}


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _payload(marker: str | None = None) -> dict[str, str]:
    unique = marker or str(uuid4())
    return {
        "title": f"Riego de papa {unique}",
        "topic": "papa",
        "content": (
            f"# Riego de papa (material de prueba)\n\n"
            f"Documento de prueba HU-05. Identificador: {unique}.\n"
        ),
    }


def _cleanup(source_path: str) -> None:
    knowledge_dir = Path(container.settings.knowledge_dir).resolve()
    path = knowledge_dir / Path(source_path).name
    path.unlink(missing_ok=True)
    path.with_suffix(".meta.json").unlink(missing_ok=True)


def test_ingest_knowledge_requires_auth() -> None:
    response = client.post(INGEST_URL, json=_payload())
    assert response.status_code == 401
    listed = client.get(DOCUMENTS_URL)
    assert listed.status_code == 401


def test_ingest_knowledge_rejects_invalid_token() -> None:
    response = client.post(
        INGEST_URL,
        json=_payload(),
        headers=_auth("token-invalido"),
    )
    assert response.status_code == 401


def test_ingest_knowledge_empty_content_returns_422() -> None:
    user = _register_and_login()
    response = client.post(
        INGEST_URL,
        json={"title": "Riego", "topic": "papa", "content": ""},
        headers=_auth(user["token"]),
    )
    assert response.status_code == 422


def test_ingest_knowledge_success_and_persistence() -> None:
    user = _register_and_login()
    payload = _payload()
    response = client.post(INGEST_URL, json=payload, headers=_auth(user["token"]))
    assert response.status_code == 201
    body = response.json()
    try:
        assert body["status"] == "registered"
        assert body["title"] == payload["title"]
        assert body["topic"] == "papa"
        assert body["chunk_count"] == 0
        assert len(body["content_hash"]) == 64
        assert body["source_path"].endswith(".md")
        assert "password" not in str(body)

        engine = create_mysql_engine(container.settings)
        with engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT ruta_origen, hash_contenido FROM documentos_conocimiento WHERE id = :id"
                ),
                {"id": body["id"]},
            ).first()
        assert row is not None
        assert row[0] == body["source_path"]
        assert row[1] == body["content_hash"]

        stored_file = Path(container.settings.knowledge_dir).resolve() / Path(body["source_path"]).name
        assert stored_file.exists()
        assert "material de prueba" in stored_file.read_text(encoding="utf-8").lower()
    finally:
        _cleanup(body["source_path"])


def test_ingest_knowledge_duplicate_returns_409() -> None:
    user = _register_and_login()
    payload = _payload()
    first = client.post(INGEST_URL, json=payload, headers=_auth(user["token"]))
    assert first.status_code == 201
    source_path = first.json()["source_path"]
    try:
        second = client.post(INGEST_URL, json=payload, headers=_auth(user["token"]))
        assert second.status_code == 409
        assert "ya está registrado" in second.json()["detail"]

        engine = create_mysql_engine(container.settings)
        with engine.connect() as connection:
            count = connection.execute(
                text("SELECT COUNT(*) FROM documentos_conocimiento WHERE hash_contenido = :hash"),
                {"hash": first.json()["content_hash"]},
            ).scalar_one()
        assert count == 1
    finally:
        _cleanup(source_path)


def test_list_knowledge_documents_returns_registered_metadata() -> None:
    user = _register_and_login()
    payload = _payload()
    created = client.post(INGEST_URL, json=payload, headers=_auth(user["token"]))
    assert created.status_code == 201
    source_path = created.json()["source_path"]
    try:
        listed = client.get(DOCUMENTS_URL, headers=_auth(user["token"]))
        assert listed.status_code == 200
        ids = [item["id"] for item in listed.json()]
        assert created.json()["id"] in ids
        match = next(item for item in listed.json() if item["id"] == created.json()["id"])
        assert match["title"] == payload["title"]
        assert match["content_hash"] == created.json()["content_hash"]
        assert "answer" not in match
    finally:
        _cleanup(source_path)
