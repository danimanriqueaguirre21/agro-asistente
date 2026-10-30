from app.domain.ports.input.ingest_knowledge_port import (
    KnowledgeDocumentResult,
    ListKnowledgeDocumentsPort,
    knowledge_to_result,
)
from app.domain.ports.output.knowledge_document_repository_port import (
    KnowledgeDocumentRepositoryPort,
)


class ListKnowledgeDocuments(ListKnowledgeDocumentsPort):
    def __init__(self, knowledge_repository: KnowledgeDocumentRepositoryPort) -> None:
        self._knowledge_repository = knowledge_repository

    def execute(self) -> list[KnowledgeDocumentResult]:
        documents = self._knowledge_repository.list_all()
        return [knowledge_to_result(document, status="registered") for document in documents]
