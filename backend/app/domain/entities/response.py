from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import InvalidQueryDataError


class Response:
    def __init__(
        self,
        response_id: str,
        query_id: str,
        answer_text: str,
        generation_method: str,
        created_at: datetime,
    ) -> None:
        self.id = response_id
        self.query_id = query_id
        self.answer_text = answer_text
        self.generation_method = generation_method
        self.created_at = created_at

    @classmethod
    def create(cls, query_id: str, answer_text: str, generation_method: str) -> "Response":
        if not (query_id or "").strip():
            raise InvalidQueryDataError("La consulta es obligatoria")
        clean_answer = (answer_text or "").strip()
        if not clean_answer:
            raise InvalidQueryDataError("La respuesta generada es obligatoria")
        clean_method = (generation_method or "").strip()
        if not clean_method:
            raise InvalidQueryDataError("El método de generación es obligatorio")
        if len(clean_method) > 40:
            raise InvalidQueryDataError("El método de generación supera la longitud permitida")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            response_id=str(uuid4()),
            query_id=query_id.strip(),
            answer_text=clean_answer,
            generation_method=clean_method,
            created_at=now,
        )
