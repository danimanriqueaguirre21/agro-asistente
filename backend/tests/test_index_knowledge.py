from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.application.services.fragmentador_documentos import FragmentadorDocumentos
from app.application.useCases.indexar_conocimiento import IndexarConocimiento
from app.domain.entities.documento_conocimiento import DocumentoConocimiento
from app.domain.ports.output.embedding_port import EmbeddingPort
from app.domain.ports.output.repositorio_documento_conocimiento_port import (
    PuertoRepositorioDocumentoConocimiento,
)
from app.domain.ports.output.vector_store_port import VectorRecord, VectorSearchHit, VectorStorePort
from app.domain.valueObjects.hash_contenido import HashContenido
from app.infrastructure.adapters.output.embedding.local_lexical_embedding_adapter import (
    LocalLexicalEmbeddingAdapter,
)

CONTENT = """# Riego de papa

La papa en sierra requiere riegos frecuentes en floración.
Evitar encharcamiento para reducir riesgo de lancha.
"""


class RepositorioConocimientoEnMemoria(PuertoRepositorioDocumentoConocimiento):
    def __init__(self) -> None:
        self.documentos: list[DocumentoConocimiento] = []
        self.contenidos: dict[str, str] = {}

    def existe_por_hash(self, hash_contenido: HashContenido) -> bool:
        return any(documento.hash_contenido == hash_contenido for documento in self.documentos)

    def guardar(self, documento: DocumentoConocimiento, contenido: str) -> None:
        self.documentos.append(documento)
        self.contenidos[documento.id] = contenido

    def listar_todos(self) -> list[DocumentoConocimiento]:
        return list(self.documentos)

    def buscar_por_id(self, documento_id: str) -> DocumentoConocimiento | None:
        for documento in self.documentos:
            if documento.id == documento_id:
                return documento
        return None

    def leer_contenido(self, documento: DocumentoConocimiento) -> str:
        return self.contenidos[documento.id]

    def actualizar_cantidad_fragmentos(self, documento_id: str, cantidad_fragmentos: int) -> None:
        for documento in self.documentos:
            if documento.id == documento_id:
                documento.cantidad_fragmentos = cantidad_fragmentos
                return


class AlmacenVectoresEnMemoria(VectorStorePort):
    def __init__(self) -> None:
        self.records: dict[str, VectorRecord] = {}

    def upsert(self, records: list[VectorRecord]) -> None:
        for record in records:
            self.records[record.id] = record

    def similarity_search(self, embedding: list[float], top_k: int) -> list[VectorSearchHit]:
        hits: list[VectorSearchHit] = []
        for record in self.records.values():
            score = _cosine(embedding, record.embedding)
            hits.append(
                VectorSearchHit(
                    id=record.id,
                    content=record.content,
                    metadata=record.metadata,
                    similarity=score,
                )
            )
        hits.sort(key=lambda item: item.similarity, reverse=True)
        return hits[:top_k]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


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


def test_index_knowledge_upserts_chunks_with_deterministic_ids() -> None:
    repository = RepositorioConocimientoEnMemoria()
    store = AlmacenVectoresEnMemoria()
    document = _documento()
    repository.guardar(document, CONTENT)
    use_case = IndexarConocimiento(
        repositorio_conocimiento=repository,
        embedding_port=LocalLexicalEmbeddingAdapter(dimension=32),
        almacen_vectores=store,
        fragmentador=FragmentadorDocumentos(max_chars=80),
    )

    result = use_case.ejecutar()

    assert result.documentos_indexados == 1
    assert result.total_fragmentos == len(store.records)
    assert result.total_fragmentos >= 1
    assert document.cantidad_fragmentos == result.total_fragmentos
    assert all(":chunk:" in chunk_id for chunk_id in store.records)


def test_index_knowledge_duplicate_document_does_not_duplicate_chunks() -> None:
    repository = RepositorioConocimientoEnMemoria()
    store = AlmacenVectoresEnMemoria()
    document = _documento()
    repository.guardar(document, CONTENT)
    use_case = IndexarConocimiento(
        repositorio_conocimiento=repository,
        embedding_port=LocalLexicalEmbeddingAdapter(dimension=32),
        almacen_vectores=store,
        fragmentador=FragmentadorDocumentos(max_chars=80),
    )

    first = use_case.ejecutar()
    ids_after_first = set(store.records)
    second = use_case.ejecutar()

    assert first.total_fragmentos == second.total_fragmentos
    assert set(store.records) == ids_after_first
    assert len(store.records) == first.total_fragmentos


def test_index_knowledge_uses_embedding_port_not_sdk() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "application"
        / "useCases"
        / "indexar_conocimiento.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    assert "embeddingport" in lowered
    assert "vectorstoreport" in lowered
    assert "chromadb" not in lowered
    assert "chromavectorstoreadapter" not in lowered
    assert "openai" not in lowered
    assert "httpx" not in lowered
    assert "fastapi" not in lowered


def test_index_knowledge_does_not_depend_on_concrete_embedding_adapter() -> None:
    class CountingEmbedding(EmbeddingPort):
        def __init__(self) -> None:
            self.calls = 0

        def embed_text(self, text: str) -> list[float]:
            return self.embed_texts([text])[0]

        def embed_texts(self, texts: list[str]) -> list[list[float]]:
            self.calls += 1
            return LocalLexicalEmbeddingAdapter(dimension=16).embed_texts(texts)

    repository = RepositorioConocimientoEnMemoria()
    store = AlmacenVectoresEnMemoria()
    repository.guardar(_documento(), CONTENT)
    embedding = CountingEmbedding()
    use_case = IndexarConocimiento(
        repositorio_conocimiento=repository,
        embedding_port=embedding,
        almacen_vectores=store,
        fragmentador=FragmentadorDocumentos(max_chars=120),
    )
    result = use_case.ejecutar()
    assert embedding.calls == 1
    assert result.total_fragmentos == len(store.records)
