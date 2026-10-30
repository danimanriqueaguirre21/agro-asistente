from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.agricultor import Agricultor
from app.domain.exceptions import ErrorCorreoDuplicado
from app.domain.ports.output.repositorio_agricultor_port import PuertoRepositorioAgricultor
from app.domain.valueObjects.email import Email
from app.domain.valueObjects.hash_contrasena import HashContrasena
from app.infrastructure.adapters.output.mysql.connection import Base, id_a_dominio


class RegistroAgricultor(Base):
    __tablename__ = "agricultores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(150), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_creacion: Mapped[object] = mapped_column(DateTime, nullable=True)


class RepositorioAgricultorMysql(PuertoRepositorioAgricultor):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def existe_por_correo(self, email: Email) -> bool:
        with self._session_factory() as session:
            agricultor_id = session.scalar(
                select(RegistroAgricultor.id).where(RegistroAgricultor.correo == email.value)
            )
            return agricultor_id is not None

    def buscar_por_correo(self, email: Email) -> Agricultor | None:
        with self._session_factory() as session:
            registro = session.scalar(
                select(RegistroAgricultor).where(RegistroAgricultor.correo == email.value)
            )
            if registro is None:
                return None
            return self._a_entidad(registro)

    def guardar(self, agricultor: Agricultor) -> None:
        registro = RegistroAgricultor(
            nombre_completo=agricultor.nombre_completo[:150],
            correo=agricultor.email.value[:150],
            contrasena_hash=agricultor.hash_contrasena.value,
            fecha_creacion=agricultor.creado_en,
        )
        with self._session_factory() as session:
            session.add(registro)
            try:
                session.flush()
                agricultor.id = id_a_dominio(registro.id)
                session.commit()
            except IntegrityError as error:
                session.rollback()
                raise ErrorCorreoDuplicado(
                    "El correo electrónico ya está registrado"
                ) from error

    def _a_entidad(self, registro: RegistroAgricultor) -> Agricultor:
        nombres, apellidos = _separar_nombre_completo(registro.nombre_completo)
        creado = registro.fecha_creacion
        return Agricultor(
            agricultor_id=id_a_dominio(registro.id),
            nombres=nombres,
            apellidos=apellidos,
            email=Email(registro.correo),
            hash_contrasena=HashContrasena(registro.contrasena_hash),
            creado_en=creado,
            actualizado_en=creado,
        )


def _separar_nombre_completo(nombre_completo: str) -> tuple[str, str]:
    partes = (nombre_completo or "").strip().split(" ", 1)
    if len(partes) == 1:
        return partes[0], ""
    return partes[0], partes[1]
