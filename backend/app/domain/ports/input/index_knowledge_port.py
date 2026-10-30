from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.ports.input.ingest_knowledge_port import KnowledgeDocumentResult


@dataclass(frozen=True)
class IndexKnowledgeResult:
    indexed_documents: int
    total_chunks: int
    documents: tuple[KnowledgeDocumentResult, ...]


class IndexKnowledgePort(ABC):
    @abstractmethod
    def execute(self) -> IndexKnowledgeResult:
        """Indexa los documentos de conocimiento registrados para la recuperación RAG."""
