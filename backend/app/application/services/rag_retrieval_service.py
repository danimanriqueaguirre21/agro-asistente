from dataclasses import dataclass

from app.domain.ports.output.embedding_port import EmbeddingPort
from app.domain.ports.output.vector_store_port import VectorSearchHit, VectorStorePort


@dataclass(frozen=True)
class RetrievedSnippet:
    document_id: str
    document_title: str
    chunk_id: str
    excerpt: str
    similarity_score: float


class RagRetrievalService:
    """Recupera fragmentos relevantes mediante EmbeddingPort y VectorStorePort."""

    def __init__(
        self,
        embedding_port: EmbeddingPort,
        vector_store: VectorStorePort,
        top_k: int = 3,
        min_similarity: float = 0.12,
    ) -> None:
        if top_k < 1:
            raise ValueError("top_k debe ser positivo")
        self._embedding_port = embedding_port
        self._vector_store = vector_store
        self._top_k = top_k
        self._min_similarity = min_similarity

    def retrieve(self, query_text: str) -> list[RetrievedSnippet]:
        embedding = self._embedding_port.embed_text(query_text)
        hits = self._vector_store.similarity_search(embedding, self._top_k)
        snippets: list[RetrievedSnippet] = []
        for hit in hits:
            if hit.similarity < self._min_similarity:
                continue
            snippet = _snippet_from_hit(hit)
            if snippet is None:
                continue
            snippets.append(snippet)
        return snippets


def _snippet_from_hit(hit: VectorSearchHit) -> RetrievedSnippet | None:
    document_id = str(hit.metadata.get("document_id", "")).strip()
    excerpt = (hit.content or "").strip()
    if not document_id or not excerpt:
        return None
    title = str(hit.metadata.get("document_title", "")).strip()
    return RetrievedSnippet(
        document_id=document_id,
        document_title=title,
        chunk_id=hit.id,
        excerpt=excerpt,
        similarity_score=round(max(0.0, min(1.0, float(hit.similarity))), 5),
    )
