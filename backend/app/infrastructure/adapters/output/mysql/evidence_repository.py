from decimal import Decimal

from sqlalchemy import Integer, Numeric, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.evidence import Evidence
from app.domain.ports.output.evidence_repository_port import EvidenceRepositoryPort
from app.infrastructure.adapters.output.mysql.connection import Base


class EvidenceRecord(Base):
    __tablename__ = "evidences"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    query_id: Mapped[str] = mapped_column(String(36), nullable=False)
    response_id: Mapped[str] = mapped_column(String(36), nullable=False)
    document_id: Mapped[str] = mapped_column(String(36), nullable=False)
    chroma_chunk_id: Mapped[str] = mapped_column(String(120), nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    similarity_score: Mapped[Decimal] = mapped_column(Numeric(6, 5), nullable=False)
    rank_order: Mapped[int] = mapped_column(Integer, nullable=False)


class MysqlEvidenceRepository(EvidenceRepositoryPort):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def save_all(self, evidences: list[Evidence]) -> None:
        if not evidences:
            return
        records = [
            EvidenceRecord(
                id=item.id,
                query_id=item.query_id,
                response_id=item.response_id,
                document_id=item.document_id,
                chroma_chunk_id=item.chunk_id,
                excerpt=item.excerpt,
                similarity_score=Decimal(str(item.similarity_score)),
                rank_order=item.rank_order,
            )
            for item in evidences
        ]
        with self._session_factory() as session:
            session.add_all(records)
            session.commit()

    def list_by_query_id(self, query_id: str) -> list[Evidence]:
        with self._session_factory() as session:
            records = session.scalars(
                select(EvidenceRecord)
                .where(EvidenceRecord.query_id == query_id)
                .order_by(EvidenceRecord.rank_order.asc())
            ).all()
            return [self._to_entity(record) for record in records]

    def _to_entity(self, record: EvidenceRecord) -> Evidence:
        return Evidence(
            evidence_id=record.id,
            query_id=record.query_id,
            response_id=record.response_id,
            document_id=record.document_id,
            chunk_id=record.chroma_chunk_id,
            excerpt=record.excerpt,
            similarity_score=float(record.similarity_score),
            rank_order=int(record.rank_order),
        )
