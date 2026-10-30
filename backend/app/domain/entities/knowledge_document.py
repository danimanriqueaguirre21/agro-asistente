from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import InvalidKnowledgeDocumentError
from app.domain.valueObjects.content_hash import ContentHash


class KnowledgeDocument:
    TITLE_MAX_LENGTH = 200
    TOPIC_MAX_LENGTH = 50
    SOURCE_PATH_MAX_LENGTH = 255
    CONTENT_MAX_LENGTH = 20000

    def __init__(
        self,
        document_id: str,
        title: str,
        source_path: str,
        topic: str,
        content_hash: ContentHash,
        chunk_count: int,
        ingested_at: datetime,
    ) -> None:
        self.id = document_id
        self.title = title
        self.source_path = source_path
        self.topic = topic
        self.content_hash = content_hash
        self.chunk_count = chunk_count
        self.ingested_at = ingested_at

    @classmethod
    def create(
        cls,
        title: str,
        topic: str,
        content_hash: ContentHash,
    ) -> "KnowledgeDocument":
        clean_title = (title or "").strip()
        clean_topic = (topic or "").strip()
        if not clean_title:
            raise InvalidKnowledgeDocumentError("El título es obligatorio")
        if len(clean_title) > cls.TITLE_MAX_LENGTH:
            raise InvalidKnowledgeDocumentError("El título supera la longitud permitida")
        if not clean_topic:
            raise InvalidKnowledgeDocumentError("El tema es obligatorio")
        if len(clean_topic) > cls.TOPIC_MAX_LENGTH:
            raise InvalidKnowledgeDocumentError("El tema supera la longitud permitida")

        document_id = str(uuid4())
        source_path = f"knowledge/{document_id}.md"
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            document_id=document_id,
            title=clean_title,
            source_path=source_path,
            topic=clean_topic,
            content_hash=content_hash,
            chunk_count=0,
            ingested_at=now,
        )
