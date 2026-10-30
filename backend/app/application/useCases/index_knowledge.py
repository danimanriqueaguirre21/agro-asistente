from app.application.services.document_chunker import DocumentChunk, DocumentChunker
from app.domain.entities.knowledge_document import KnowledgeDocument
from app.domain.exceptions import KnowledgeFileNotFoundError
from app.domain.ports.input.index_knowledge_port import IndexKnowledgePort, IndexKnowledgeResult
from app.domain.ports.input.ingest_knowledge_port import knowledge_to_result
from app.domain.ports.output.embedding_port import EmbeddingPort
from app.domain.ports.output.knowledge_document_repository_port import (
    KnowledgeDocumentRepositoryPort,
)
from app.domain.ports.output.vector_store_port import VectorRecord, VectorStorePort


class IndexKnowledge(IndexKnowledgePort):
    def __init__(
        self,
        knowledge_repository: KnowledgeDocumentRepositoryPort,
        embedding_port: EmbeddingPort,
        vector_store: VectorStorePort,
        chunker: DocumentChunker,
    ) -> None:
        self._knowledge_repository = knowledge_repository
        self._embedding_port = embedding_port
        self._vector_store = vector_store
        self._chunker = chunker

    def execute(self) -> IndexKnowledgeResult:
        documents = self._knowledge_repository.list_all()
        indexed: list[KnowledgeDocument] = []
        total_chunks = 0
        for document in documents:
            chunks = self._index_document(document)
            if chunks is None:
                continue
            total_chunks += len(chunks)
            document.chunk_count = len(chunks)
            self._knowledge_repository.update_chunk_count(document.id, len(chunks))
            indexed.append(document)
        return IndexKnowledgeResult(
            indexed_documents=len(indexed),
            total_chunks=total_chunks,
            documents=tuple(knowledge_to_result(item, status="indexed") for item in indexed),
        )

    def _index_document(self, document: KnowledgeDocument) -> list[DocumentChunk] | None:
        try:
            content = self._knowledge_repository.read_content(document)
        except (FileNotFoundError, KnowledgeFileNotFoundError):
            return None
        chunks = self._chunker.chunk(content, document)
        if not chunks:
            return []
        embeddings = self._embedding_port.embed_texts([chunk.content for chunk in chunks])
        records = [
            VectorRecord(
                id=chunk.chunk_id,
                embedding=embedding,
                content=chunk.content,
                metadata={
                    "document_id": chunk.document_id,
                    "document_title": chunk.title,
                    "topic": chunk.topic,
                    "content_hash": chunk.content_hash,
                    "chunk_index": chunk.chunk_index,
                    "source_path": chunk.source_path,
                },
            )
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        self._vector_store.upsert(records)
        return chunks
