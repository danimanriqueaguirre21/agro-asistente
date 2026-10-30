from pathlib import Path

from app.application.services.servicio_recuperacion_rag import ServicioRecuperacionRag
from app.domain.ports.output.vector_store_port import VectorRecord, VectorSearchHit, VectorStorePort
from app.infrastructure.adapters.output.embedding.local_lexical_embedding_adapter import (
    LocalLexicalEmbeddingAdapter,
)


class AlmacenVectoresEnMemoria(VectorStorePort):
    def __init__(self) -> None:
        self.records: dict[str, VectorRecord] = {}
        self.queries: list[list[float]] = []

    def upsert(self, records: list[VectorRecord]) -> None:
        for record in records:
            self.records[record.id] = record

    def similarity_search(self, embedding: list[float], top_k: int) -> list[VectorSearchHit]:
        self.queries.append(embedding)
        hits = [
            VectorSearchHit(
                id=record.id,
                content=record.content,
                metadata=record.metadata,
                similarity=_cosine(embedding, record.embedding),
            )
            for record in self.records.values()
        ]
        hits.sort(key=lambda item: item.similarity, reverse=True)
        return hits[:top_k]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def test_vector_store_port_search_returns_similar_chunks() -> None:
    embedding = LocalLexicalEmbeddingAdapter(dimension=32)
    store = AlmacenVectoresEnMemoria()
    papa = embedding.embed_text("Riego frecuente de papa en floración")
    helada = embedding.embed_text("Cubrir plantones antes de una helada")
    store.upsert(
        [
            VectorRecord(
                id="hash-a:chunk:0000",
                embedding=papa,
                content="Riego frecuente de papa en floración.",
                metadata={"document_id": "doc-papa", "document_title": "Riego de papa"},
            ),
            VectorRecord(
                id="hash-b:chunk:0000",
                embedding=helada,
                content="Cubrir plantones antes de una helada.",
                metadata={"document_id": "doc-helada", "document_title": "Heladas"},
            ),
        ]
    )
    hits = store.similarity_search(embedding.embed_text("¿Cómo riego la papa en floración?"), top_k=1)
    assert len(hits) == 1
    assert hits[0].metadata["document_id"] == "doc-papa"
    assert "papa" in hits[0].content.lower()


def test_rag_retrieval_converts_hits_into_evidences() -> None:
    embedding = LocalLexicalEmbeddingAdapter(dimension=32)
    store = AlmacenVectoresEnMemoria()
    vector = embedding.embed_text("Riego frecuente de papa en floración")
    store.upsert(
        [
            VectorRecord(
                id="hash-a:chunk:0000",
                embedding=vector,
                content="Riego frecuente de papa en floración.",
                metadata={"document_id": "doc-papa", "document_title": "Riego de papa"},
            )
        ]
    )
    service = ServicioRecuperacionRag(
        embedding_port=embedding,
        almacen_vectores=store,
        top_k=3,
        similitud_minima=0.1,
    )
    snippets = service.recuperar("¿Cómo riego la papa en floración?")
    assert len(snippets) == 1
    assert snippets[0].documento_id == "doc-papa"
    assert snippets[0].titulo_documento == "Riego de papa"
    assert "Riego frecuente" in snippets[0].extracto
    assert snippets[0].puntaje_similitud > 0
    assert store.queries


def test_rag_retrieval_does_not_invent_evidence_below_threshold() -> None:
    embedding = LocalLexicalEmbeddingAdapter(dimension=32)
    store = AlmacenVectoresEnMemoria()
    store.upsert(
        [
            VectorRecord(
                id="hash-a:chunk:0000",
                embedding=embedding.embed_text("xyzabc qwerty token-unico-irrelevante"),
                content="Contenido no relacionado.",
                metadata={"document_id": "doc-x", "document_title": "Otro"},
            )
        ]
    )
    service = ServicioRecuperacionRag(
        embedding_port=embedding,
        almacen_vectores=store,
        top_k=3,
        similitud_minima=0.99,
    )
    snippets = service.recuperar("¿Cómo riego la papa en floración?")
    assert snippets == []


def test_rag_retrieval_service_does_not_import_chroma_or_sdk() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "application"
        / "services"
        / "servicio_recuperacion_rag.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    assert "embeddingport" in lowered
    assert "vectorstoreport" in lowered
    assert "chromadb" not in lowered
    assert "openai" not in lowered
    assert "httpx" not in lowered
    assert "fastapi" not in lowered
