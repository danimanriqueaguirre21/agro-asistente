from sqlalchemy import DateTime, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.agricultural_context import AgriculturalContext
from app.domain.entities.query import Query
from app.domain.entities.response import Response
from app.domain.ports.output.query_repository_port import QueryRepositoryPort
from app.domain.valueObjects.crop import Crop
from app.domain.valueObjects.region import Region
from app.infrastructure.adapters.output.mysql.agricultural_context_repository import (
    AgriculturalContextRecord,
)
from app.infrastructure.adapters.output.mysql.connection import Base


class QueryRecord(Base):
    __tablename__ = "queries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    farmer_id: Mapped[str] = mapped_column(String(36), nullable=False)
    context_id: Mapped[str] = mapped_column(String(36), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False)


class ResponseRecord(Base):
    __tablename__ = "responses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    query_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    generation_method: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False)


class MysqlQueryRepository(QueryRepositoryPort):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def find_selected_context(self, farmer_id: str) -> AgriculturalContext | None:
        with self._session_factory() as session:
            record = session.scalar(
                select(AgriculturalContextRecord).where(
                    AgriculturalContextRecord.farmer_id == farmer_id,
                    AgriculturalContextRecord.is_selected.is_(True),
                )
            )
            if record is None:
                return None
            return AgriculturalContext(
                context_id=record.id,
                farmer_id=record.farmer_id,
                plot_name=record.plot_name,
                crop=Crop(record.crop),
                region=Region(record.region),
                notes=record.notes,
                is_selected=bool(record.is_selected),
                created_at=record.created_at,
            )

    def save_query(self, query: Query) -> None:
        record = QueryRecord(
            id=query.id,
            farmer_id=query.farmer_id,
            context_id=query.context_id,
            question_text=query.text.value,
            created_at=query.created_at,
        )
        with self._session_factory() as session:
            session.add(record)
            session.commit()

    def save_response(self, response: Response) -> None:
        record = ResponseRecord(
            id=response.id,
            query_id=response.query_id,
            answer_text=response.answer_text,
            generation_method=response.generation_method,
            created_at=response.created_at,
        )
        with self._session_factory() as session:
            session.add(record)
            session.commit()
