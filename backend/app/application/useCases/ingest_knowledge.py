from app.domain.entities.knowledge_document import KnowledgeDocument
from app.domain.exceptions import DuplicateKnowledgeDocumentError, InvalidKnowledgeDocumentError
from app.domain.ports.input.ingest_knowledge_port import (
    IngestKnowledgeCommand,
    IngestKnowledgePort,
    KnowledgeDocumentResult,
    knowledge_to_result,
)
from app.domain.ports.output.knowledge_document_repository_port import (
    KnowledgeDocumentRepositoryPort,
)
from app.domain.valueObjects.content_hash import ContentHash


class IngestKnowledge(IngestKnowledgePort):
    def __init__(self, knowledge_repository: KnowledgeDocumentRepositoryPort) -> None:
        self._knowledge_repository = knowledge_repository

    def execute(self, command: IngestKnowledgeCommand) -> KnowledgeDocumentResult:
        content = _validated_content(command.content)
        content_hash = ContentHash.from_content(content)
        if self._knowledge_repository.exists_by_hash(content_hash):
            raise DuplicateKnowledgeDocumentError(
                "El documento de conocimiento ya está registrado"
            )

        document = KnowledgeDocument.create(
            title=command.title,
            topic=command.topic,
            content_hash=content_hash,
        )
        self._knowledge_repository.save(document, content)
        return knowledge_to_result(document, status="registered")


def _validated_content(content: str) -> str:
    if content is None:
        raise InvalidKnowledgeDocumentError("El contenido es obligatorio")
    clean = str(content).strip()
    if not clean:
        raise InvalidKnowledgeDocumentError("El contenido es obligatorio")
    if len(clean) > KnowledgeDocument.CONTENT_MAX_LENGTH:
        raise InvalidKnowledgeDocumentError("El contenido supera la longitud permitida")
    return clean
