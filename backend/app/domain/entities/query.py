from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import InvalidQueryDataError
from app.domain.valueObjects.query_text import QueryText


class Query:
    def __init__(
        self,
        query_id: str,
        farmer_id: str,
        context_id: str,
        text: QueryText,
        created_at: datetime,
    ) -> None:
        self.id = query_id
        self.farmer_id = farmer_id
        self.context_id = context_id
        self.text = text
        self.created_at = created_at

    @classmethod
    def create(cls, farmer_id: str, context_id: str, text: QueryText) -> "Query":
        if not (farmer_id or "").strip():
            raise InvalidQueryDataError("El agricultor es obligatorio")
        if not (context_id or "").strip():
            raise InvalidQueryDataError("El contexto agrícola es obligatorio")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            query_id=str(uuid4()),
            farmer_id=farmer_id.strip(),
            context_id=context_id.strip(),
            text=text,
            created_at=now,
        )
