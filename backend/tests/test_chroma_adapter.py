from pathlib import Path

from app.domain.ports.output.vector_store_port import VectorRecord
from app.infrastructure.adapters.output.chroma.chroma_vector_store_adapter import (
    PMV1_COLLECTION,
    ChromaVectorStoreAdapter,
)
from app.infrastructure.adapters.output.embedding.local_lexical_embedding_adapter import (
    LocalLexicalEmbeddingAdapter,
)


def test_chroma_adapter_creates_collection_inserts_and_searches(tmp_path: Path) -> None:
    persist_dir = tmp_path / "chroma_test_data"
    adapter = ChromaVectorStoreAdapter(
        persist_dir=str(persist_dir),
        collection_name="agro_knowledge_pmv1_test",
    )
    embedding = LocalLexicalEmbeddingAdapter(dimension=32)
    papa = embedding.embed_text("Riego frecuente de papa en floración")
    helada = embedding.embed_text("Cubrir plantones antes de heladas en sierra")

    adapter.upsert(
        [
            VectorRecord(
                id="aaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccdddd:chunk:0000",
                embedding=papa,
                content="La papa en sierra requiere riegos frecuentes en floración.",
                metadata={
                    "document_id": "doc-papa",
                    "document_title": "Riego de papa",
                    "topic": "papa",
                    "content_hash": "aaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccdddd",
                    "chunk_index": 0,
                    "source_path": "knowledge/doc-papa.md",
                },
            ),
            VectorRecord(
                id="bbbbccccddddeeeebbbbccccddddeeeebbbbccccddddeeeebbbbccccddddeeee:chunk:0000",
                embedding=helada,
                content="Cubrir plantones jóvenes antes de madrugadas frías.",
                metadata={
                    "document_id": "doc-helada",
                    "document_title": "Heladas en sierra",
                    "topic": "heladas",
                    "content_hash": "bbbbccccddddeeeebbbbccccddddeeeebbbbccccddddeeeebbbbccccddddeeee",
                    "chunk_index": 0,
                    "source_path": "knowledge/doc-helada.md",
                },
            ),
        ]
    )

    assert adapter._collection.name == "agro_knowledge_pmv1_test"
    assert adapter.collection_name == "agro_knowledge_pmv1_test"
    assert adapter.collection_name != PMV1_COLLECTION

    hits = adapter.similarity_search(
        embedding.embed_text("¿Cómo riego la papa en floración?"),
        top_k=2,
    )
    assert hits
    top = hits[0]
    assert top.metadata["document_id"] == "doc-papa"
    assert top.metadata["document_title"] == "Riego de papa"
    assert "floración" in top.content
    assert top.similarity > 0


def test_chroma_adapter_upsert_is_idempotent(tmp_path: Path) -> None:
    adapter = ChromaVectorStoreAdapter(
        persist_dir=str(tmp_path / "chroma_test_data"),
        collection_name="agro_knowledge_pmv1_test",
    )
    embedding = LocalLexicalEmbeddingAdapter(dimension=32)
    record = VectorRecord(
        id="ccccddddeeeeffffccccddddeeeeffffccccddddeeeeffffccccddddeeeeffff:chunk:0000",
        embedding=embedding.embed_text("Riego de papa"),
        content="Riego de papa en floración.",
        metadata={"document_id": "doc-1", "document_title": "Riego", "chunk_index": 0},
    )
    adapter.upsert([record])
    adapter.upsert([record])
    assert adapter._collection.count() == 1


def test_chroma_test_collection_does_not_use_pmv1_name() -> None:
    assert PMV1_COLLECTION == "agro_knowledge_pmv1"
