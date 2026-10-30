from sqlalchemy import DateTime, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.farmer import Farmer
from app.domain.exceptions import DuplicateEmailError
from app.domain.ports.output.farmer_repository_port import FarmerRepositoryPort
from app.domain.valueObjects.email import Email
from app.domain.valueObjects.password_hash import PasswordHash
from app.infrastructure.adapters.output.mysql.connection import Base


class FarmerRecord(Base):
    __tablename__ = "farmers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(190), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime, nullable=False)


class MysqlFarmerRepository(FarmerRepositoryPort):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def exists_by_email(self, email: Email) -> bool:
        with self._session_factory() as session:
            farmer_id = session.scalar(
                select(FarmerRecord.id).where(FarmerRecord.email == email.value)
            )
            return farmer_id is not None

    def find_by_email(self, email: Email) -> Farmer | None:
        with self._session_factory() as session:
            record = session.scalar(
                select(FarmerRecord).where(FarmerRecord.email == email.value)
            )
            if record is None:
                return None
            return self._to_entity(record)

    def save(self, farmer: Farmer) -> None:
        record = FarmerRecord(
            id=farmer.id,
            full_name=farmer.full_name,
            email=farmer.email.value,
            password_hash=farmer.password_hash.value,
            created_at=farmer.created_at,
            updated_at=farmer.updated_at,
        )
        with self._session_factory() as session:
            session.add(record)
            try:
                session.commit()
            except IntegrityError as error:
                session.rollback()
                raise DuplicateEmailError(
                    "El correo electrónico ya está registrado"
                ) from error

    def _to_entity(self, record: FarmerRecord) -> Farmer:
        names, last_names = _split_full_name(record.full_name)
        return Farmer(
            farmer_id=record.id,
            names=names,
            last_names=last_names,
            email=Email(record.email),
            password_hash=PasswordHash(record.password_hash),
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


def _split_full_name(full_name: str) -> tuple[str, str]:
    parts = (full_name or "").strip().split(" ", 1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]
