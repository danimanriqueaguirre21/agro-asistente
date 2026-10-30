from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.application.services.fragmentador_documentos import (
    FragmentadorDocumentos,
    crear_id_fragmento,
)
from app.domain.entities.documento_conocimiento import DocumentoConocimiento
from app.domain.valueObjects.hash_contenido import HashContenido

CONTENT = """# Riego de papa

La papa en sierra requiere riegos frecuentes en floración.

Evitar encharcamiento para reducir riesgo de lancha.

Registrar el contexto agrícola del agricultor.
"""


def _documento(content: str = CONTENT) -> DocumentoConocimiento:
    return DocumentoConocimiento(
        documento_id=str(uuid4()),
        titulo="Riego de papa",
        ruta_origen="knowledge/demo.md",
        tema="papa",
        hash_contenido=HashContenido.desde_contenido(content),
        cantidad_fragmentos=0,
        incorporado_en=datetime.now(timezone.utc).replace(tzinfo=None),
    )


def test_document_is_split_into_chunks() -> None:
    chunker = FragmentadorDocumentos(max_chars=80)
    chunks = chunker.fragmentar(CONTENT, _documento())
    assert len(chunks) >= 2
    joined = " ".join(item.contenido for item in chunks)
    assert "floración" in joined
    assert "encharcamiento" in joined
    assert all(item.documento_id == chunks[0].documento_id for item in chunks)
    assert [item.indice_fragmento for item in chunks] == list(range(len(chunks)))


def test_chunk_ids_are_deterministic() -> None:
    document = _documento()
    chunker = FragmentadorDocumentos(max_chars=80)
    first = chunker.fragmentar(CONTENT, document)
    second = chunker.fragmentar(CONTENT, document)
    assert [item.fragmento_id for item in first] == [item.fragmento_id for item in second]
    assert first[0].fragmento_id == crear_id_fragmento(document.hash_contenido.value, 0)
    assert first[0].fragmento_id.startswith(document.hash_contenido.value)


def test_changed_content_changes_chunk_ids() -> None:
    original = _documento(CONTENT)
    changed_content = CONTENT + "\n\nNuevo párrafo sobre abonamiento."
    changed = _documento(changed_content)
    chunker = FragmentadorDocumentos(max_chars=80)
    original_ids = {item.fragmento_id for item in chunker.fragmentar(CONTENT, original)}
    changed_ids = {item.fragmento_id for item in chunker.fragmentar(changed_content, changed)}
    assert original.hash_contenido != changed.hash_contenido
    assert original_ids.isdisjoint(changed_ids)


def test_chunker_does_not_import_chroma() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "application"
        / "services"
        / "fragmentador_documentos.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    assert "chromadb" not in lowered
    assert "chroma" not in lowered
    assert "openai" not in lowered
