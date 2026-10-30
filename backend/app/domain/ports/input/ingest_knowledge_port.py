from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.knowledge_document import KnowledgeDocument


@dataclass(frozen=True)
class IngestKnowledgeCommand:
    title: str
    topic: str
    content: str


@dataclass(frozen=True)
class KnowledgeDocumentResult:
    id: str
    title: str
    topic: str
    source_path: str
    content_hash: str
    chunk_count: int
    ingested_at: str
    status: str


class IngestKnowledgePort(ABC):
    @abstractmethod
    def execute(self, command: IngestKnowledgeCommand) -> KnowledgeDocumentResult:
        """Incorpora un documento de conocimiento agrícola."""


class ListKnowledgeDocumentsPort(ABC):
    @abstractmethod
    def execute(self) -> list[KnowledgeDocumentResult]:
        """Lista los documentos de conocimiento registrados."""


def knowledge_to_result(
    document: KnowledgeDocument,
    status: str = "registered",
) -> KnowledgeDocumentResult:
    return KnowledgeDocumentResult(
        id=document.id,
        title=document.title,
        topic=document.topic,
        source_path=document.source_path,
        content_hash=document.content_hash.value,
        chunk_count=document.chunk_count,
        ingested_at=document.ingested_at.isoformat(),
        status=status,
    )
