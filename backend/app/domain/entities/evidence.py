from uuid import uuid4

from app.domain.exceptions import InvalidEvidenceError


class Evidence:
    """Información recuperada de la base de conocimiento y asociada a una consulta."""

    CHUNK_ID_MAX_LENGTH = 120

    def __init__(
        self,
        evidence_id: str,
        query_id: str,
        response_id: str,
        document_id: str,
        chunk_id: str,
        excerpt: str,
        similarity_score: float,
        rank_order: int,
        document_title: str = "",
    ) -> None:
        self.id = evidence_id
        self.query_id = query_id
        self.response_id = response_id
        self.document_id = document_id
        self.chunk_id = chunk_id
        self.excerpt = excerpt
        self.similarity_score = similarity_score
        self.rank_order = rank_order
        self.document_title = document_title

    @classmethod
    def create(
        cls,
        query_id: str,
        response_id: str,
        document_id: str,
        chunk_id: str,
        excerpt: str,
        similarity_score: float,
        rank_order: int,
        document_title: str = "",
    ) -> "Evidence":
        if not (query_id or "").strip():
            raise InvalidEvidenceError("La consulta es obligatoria")
        if not (response_id or "").strip():
            raise InvalidEvidenceError("La respuesta es obligatoria")
        if not (document_id or "").strip():
            raise InvalidEvidenceError("El documento de origen es obligatorio")
        clean_chunk_id = (chunk_id or "").strip()
        if not clean_chunk_id:
            raise InvalidEvidenceError("El identificador del fragmento es obligatorio")
        if len(clean_chunk_id) > cls.CHUNK_ID_MAX_LENGTH:
            raise InvalidEvidenceError("El identificador del fragmento supera la longitud permitida")
        clean_excerpt = (excerpt or "").strip()
        if not clean_excerpt:
            raise InvalidEvidenceError("El contenido recuperado es obligatorio")
        try:
            score = float(similarity_score)
        except (TypeError, ValueError) as error:
            raise InvalidEvidenceError("La relevancia es inválida") from error
        if score < 0 or score > 1:
            raise InvalidEvidenceError("La relevancia debe estar entre 0 y 1")
        if not isinstance(rank_order, int) or isinstance(rank_order, bool) or rank_order < 1:
            raise InvalidEvidenceError("El orden de relevancia es inválido")
        return cls(
            evidence_id=str(uuid4()),
            query_id=query_id.strip(),
            response_id=response_id.strip(),
            document_id=document_id.strip(),
            chunk_id=clean_chunk_id,
            excerpt=clean_excerpt,
            similarity_score=round(score, 5),
            rank_order=rank_order,
            document_title=(document_title or "").strip(),
        )
