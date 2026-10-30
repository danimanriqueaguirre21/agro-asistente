from sqlalchemy import Boolean, DateTime, String, select, update
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.agricultural_context import AgriculturalContext
from app.domain.ports.output.agricultural_context_repository_port import (
    AgriculturalContextRepositoryPort,
)
from app.domain.valueObjects.crop import Crop
from app.domain.valueObjects.region import Region
from app.infrastructure.adapters.output.mysql.connection import Base


class AgriculturalContextRecord(Base):
    __tablename__ = "agricultural_contexts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    farmer_id: Mapped[str] = mapped_column(String(36), nullable=False)
    plot_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    crop: Mapped[str] = mapped_column(String(50), nullable=False)
    region: Mapped[str] = mapped_column(String(120), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False)


class MysqlAgriculturalContextRepository(AgriculturalContextRepositoryPort):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def save(self, context: AgriculturalContext) -> None:
        record = AgriculturalContextRecord(
            id=context.id,
            farmer_id=context.farmer_id,
            plot_name=context.plot_name,
            crop=context.crop.value,
            region=context.region.value,
            notes=context.notes,
            is_selected=context.is_selected,
            created_at=context.created_at,
        )
        with self._session_factory() as session:
            session.add(record)
            session.commit()

    def list_by_farmer(self, farmer_id: str) -> list[AgriculturalContext]:
        with self._session_factory() as session:
            records = session.scalars(
                select(AgriculturalContextRecord)
                .where(AgriculturalContextRecord.farmer_id == farmer_id)
                .order_by(AgriculturalContextRecord.created_at.desc())
            ).all()
            return [self._to_entity(record) for record in records]

    def find_by_id_for_farmer(self, context_id: str, farmer_id: str) -> AgriculturalContext | None:
        with self._session_factory() as session:
            record = session.scalar(
                select(AgriculturalContextRecord).where(
                    AgriculturalContextRecord.id == context_id,
                    AgriculturalContextRecord.farmer_id == farmer_id,
                )
            )
            if record is None:
                return None
            return self._to_entity(record)

    def select_for_farmer(self, context_id: str, farmer_id: str) -> AgriculturalContext | None:
        with self._session_factory() as session:
            record = session.scalar(
                select(AgriculturalContextRecord).where(
                    AgriculturalContextRecord.id == context_id,
                    AgriculturalContextRecord.farmer_id == farmer_id,
                )
            )
            if record is None:
                return None
            session.execute(
                update(AgriculturalContextRecord)
                .where(AgriculturalContextRecord.farmer_id == farmer_id)
                .values(is_selected=False)
            )
            record.is_selected = True
            session.commit()
            session.refresh(record)
            return self._to_entity(record)

    def _to_entity(self, record: AgriculturalContextRecord) -> AgriculturalContext:
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
