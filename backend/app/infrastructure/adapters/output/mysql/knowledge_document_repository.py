from pathlib import Path

from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.knowledge_document import KnowledgeDocument
from app.domain.exceptions import DuplicateKnowledgeDocumentError, KnowledgeFileNotFoundError
from app.domain.ports.output.knowledge_document_repository_port import (
    KnowledgeDocumentRepositoryPort,
)
from app.domain.valueObjects.content_hash import ContentHash
from app.infrastructure.adapters.output.mysql.connection import Base


class KnowledgeDocumentRecord(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source_path: Mapped[str] = mapped_column(String(255), nullable=False)
    topic: Mapped[str] = mapped_column(String(50), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    chunk_count: Mapped[int] = mapped_column(Integer, nullable=False)
    ingested_at: Mapped[object] = mapped_column(DateTime, nullable=False)


class MysqlKnowledgeDocumentRepository(KnowledgeDocumentRepositoryPort):
    def __init__(self, session_factory: sessionmaker, knowledge_dir: str) -> None:
        self._session_factory = session_factory
        self._knowledge_dir = Path(knowledge_dir)

    def exists_by_hash(self, content_hash: ContentHash) -> bool:
        with self._session_factory() as session:
            document_id = session.scalar(
                select(KnowledgeDocumentRecord.id).where(
                    KnowledgeDocumentRecord.content_hash == content_hash.value
                )
            )
            return document_id is not None

    def save(self, document: KnowledgeDocument, content: str) -> None:
        file_path = self._file_path(document.source_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        record = KnowledgeDocumentRecord(
            id=document.id,
            title=document.title,
            source_path=document.source_path,
            topic=document.topic,
            content_hash=document.content_hash.value,
            chunk_count=document.chunk_count,
            ingested_at=document.ingested_at,
        )
        with self._session_factory() as session:
            session.add(record)
            try:
                session.commit()
            except IntegrityError as error:
                session.rollback()
                file_path.unlink(missing_ok=True)
                raise DuplicateKnowledgeDocumentError(
                    "El documento de conocimiento ya está registrado"
                ) from error

    def list_all(self) -> list[KnowledgeDocument]:
        with self._session_factory() as session:
            records = session.scalars(
                select(KnowledgeDocumentRecord).order_by(
                    KnowledgeDocumentRecord.ingested_at.desc()
                )
            ).all()
            return [self._to_entity(record) for record in records]

    def find_by_id(self, document_id: str) -> KnowledgeDocument | None:
        with self._session_factory() as session:
            record = session.scalar(
                select(KnowledgeDocumentRecord).where(KnowledgeDocumentRecord.id == document_id)
            )
            if record is None:
                return None
            return self._to_entity(record)

    def read_content(self, document: KnowledgeDocument) -> str:
        file_path = self._file_path(document.source_path)
        if not file_path.exists():
            raise KnowledgeFileNotFoundError(
                "No se encontró el archivo del documento de conocimiento"
            )
        return file_path.read_text(encoding="utf-8")

    def update_chunk_count(self, document_id: str, chunk_count: int) -> None:
        with self._session_factory() as session:
            record = session.scalar(
                select(KnowledgeDocumentRecord).where(KnowledgeDocumentRecord.id == document_id)
            )
            if record is None:
                return
            record.chunk_count = chunk_count
            session.commit()

    def _file_path(self, source_path: str) -> Path:
        filename = Path(source_path).name
        return self._knowledge_dir / filename

    def _to_entity(self, record: KnowledgeDocumentRecord) -> KnowledgeDocument:
        return KnowledgeDocument(
            document_id=record.id,
            title=record.title,
            source_path=record.source_path,
            topic=record.topic,
            content_hash=ContentHash(record.content_hash),
            chunk_count=int(record.chunk_count),
            ingested_at=record.ingested_at,
        )
