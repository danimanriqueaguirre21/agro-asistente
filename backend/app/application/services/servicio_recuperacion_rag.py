from dataclasses import dataclass

from app.domain.ports.output.embedding_port import EmbeddingPort
from app.domain.ports.output.vector_store_port import VectorSearchHit, VectorStorePort


@dataclass(frozen=True)
class FragmentoRecuperado:
    documento_id: str
    titulo_documento: str
    fragmento_id: str
    extracto: str
    puntaje_similitud: float


class ServicioRecuperacionRag:
    """Recupera fragmentos relevantes mediante EmbeddingPort y VectorStorePort."""

    def __init__(
        self,
        embedding_port: EmbeddingPort,
        almacen_vectores: VectorStorePort,
        top_k: int = 3,
        similitud_minima: float = 0.12,
    ) -> None:
        if top_k < 1:
            raise ValueError("top_k debe ser positivo")
        self._embedding_port = embedding_port
        self._almacen_vectores = almacen_vectores
        self._top_k = top_k
        self._similitud_minima = similitud_minima

    def recuperar(self, texto_consulta: str) -> list[FragmentoRecuperado]:
        embedding = self._embedding_port.embed_text(texto_consulta)
        hits = self._almacen_vectores.similarity_search(embedding, self._top_k)
        fragmentos: list[FragmentoRecuperado] = []
        for hit in hits:
            if hit.similarity < self._similitud_minima:
                continue
            fragmento = _fragmento_desde_hit(hit)
            if fragmento is None:
                continue
            fragmentos.append(fragmento)
        return fragmentos


def _fragmento_desde_hit(hit: VectorSearchHit) -> FragmentoRecuperado | None:
    documento_id = str(hit.metadata.get("document_id", "")).strip()
    extracto = (hit.content or "").strip()
    if not documento_id or not extracto:
        return None
    titulo = str(hit.metadata.get("document_title", "")).strip()
    return FragmentoRecuperado(
        documento_id=documento_id,
        titulo_documento=titulo,
        fragmento_id=hit.id,
        extracto=extracto,
        puntaje_similitud=round(max(0.0, min(1.0, float(hit.similarity))), 5),
    )
