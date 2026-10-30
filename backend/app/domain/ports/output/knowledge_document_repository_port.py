from abc import ABC, abstractmethod

from app.domain.entities.knowledge_document import KnowledgeDocument
from app.domain.valueObjects.content_hash import ContentHash


class KnowledgeDocumentRepositoryPort(ABC):
    @abstractmethod
    def exists_by_hash(self, content_hash: ContentHash) -> bool:
        """True si ya hay un documento con el mismo hash de contenido."""

    @abstractmethod
    def save(self, document: KnowledgeDocument, content: str) -> None:
        """Persiste metadatos y el contenido del documento."""

    @abstractmethod
    def list_all(self) -> list[KnowledgeDocument]:
        """Devuelve los documentos registrados."""

    @abstractmethod
    def find_by_id(self, document_id: str) -> KnowledgeDocument | None:
        """Obtiene un documento por id. None si no existe."""

    @abstractmethod
    def read_content(self, document: KnowledgeDocument) -> str:
        """Lee el contenido Markdown persistido del documento."""

    @abstractmethod
    def update_chunk_count(self, document_id: str, chunk_count: int) -> None:
        """Actualiza la cantidad de fragmentos indexados del documento."""
