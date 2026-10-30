from chromadb import PersistentClient
from chromadb.api import ClientAPI
from chromadb.config import Settings as ChromaSettings

from app.domain.ports.output.vector_store_port import VectorRecord, VectorSearchHit, VectorStorePort

PMV1_COLLECTION = "agro_knowledge_pmv1"


class ChromaVectorStoreAdapter(VectorStorePort):
    """Adaptador concreto de VectorStorePort sobre Chroma persistente.

    Los embeddings se reciben ya calculados por EmbeddingPort. Chroma no se usa
    como generador de vectores en HU-06.
    """

    def __init__(
        self,
        persist_dir: str,
        collection_name: str = PMV1_COLLECTION,
        client: ClientAPI | None = None,
    ) -> None:
        self._collection_name = collection_name or PMV1_COLLECTION
        self._client = client or PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def collection_name(self) -> str:
        return self._collection_name

    def upsert(self, records: list[VectorRecord]) -> None:
        if not records:
            return
        self._collection.upsert(
            ids=[record.id for record in records],
            embeddings=[record.embedding for record in records],
            documents=[record.content for record in records],
            metadatas=[_chroma_metadata(record.metadata) for record in records],
        )

    def similarity_search(self, embedding: list[float], top_k: int) -> list[VectorSearchHit]:
        if top_k < 1 or not embedding:
            return []
        count = self._collection.count()
        if count == 0:
            return []
        n_results = min(top_k, count)
        raw = self._collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )
        ids = (raw.get("ids") or [[]])[0]
        documents = (raw.get("documents") or [[]])[0]
        metadatas = (raw.get("metadatas") or [[]])[0]
        distances = (raw.get("distances") or [[]])[0]
        hits: list[VectorSearchHit] = []
        for index, chunk_id in enumerate(ids):
            distance = float(distances[index]) if index < len(distances) else 1.0
            similarity = max(0.0, min(1.0, 1.0 - distance))
            metadata = metadatas[index] if index < len(metadatas) and metadatas[index] else {}
            content = documents[index] if index < len(documents) else ""
            hits.append(
                VectorSearchHit(
                    id=str(chunk_id),
                    content=str(content or ""),
                    metadata=dict(metadata),
                    similarity=similarity,
                )
            )
        return hits


def _chroma_metadata(metadata: dict[str, str | int | float]) -> dict[str, str | int | float]:
    clean: dict[str, str | int | float] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, bool):
            clean[key] = int(value)
        elif isinstance(value, (int, float, str)):
            clean[key] = value
        else:
            clean[key] = str(value)
    return clean
