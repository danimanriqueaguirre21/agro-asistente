from sqlalchemy import Boolean, DateTime, Integer, String, Text, select, update
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from app.domain.entities.contexto_agricola import ContextoAgricola
from app.domain.ports.output.repositorio_contexto_agricola_port import (
    PuertoRepositorioContextoAgricola,
)
from app.domain.valueObjects.cultivo import Cultivo
from app.domain.valueObjects.region import Region
from app.infrastructure.adapters.output.mysql.connection import (
    Base,
    id_a_dominio,
    id_a_entero,
)


class RegistroContextoAgricola(Base):
    __tablename__ = "contextos_agricolas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agricultor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_parcela: Mapped[str] = mapped_column(String(150), nullable=False)
    cultivo: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    esta_seleccionado: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    fecha_creacion: Mapped[object] = mapped_column(DateTime, nullable=True)


class RepositorioContextoAgricolaMysql(PuertoRepositorioContextoAgricola):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def guardar(self, contexto: ContextoAgricola) -> None:
        registro = RegistroContextoAgricola(
            agricultor_id=id_a_entero(contexto.agricultor_id),
            nombre_parcela=(contexto.nombre_predio or "")[:150],
            cultivo=contexto.cultivo.value[:100],
            region=contexto.region.value[:100],
            observaciones=contexto.observaciones,
            esta_seleccionado=bool(contexto.esta_seleccionado),
            fecha_creacion=contexto.creado_en,
        )
        with self._session_factory() as session:
            session.add(registro)
            session.flush()
            contexto.id = id_a_dominio(registro.id)
            session.commit()

    def listar_por_agricultor(self, agricultor_id: str) -> list[ContextoAgricola]:
        with self._session_factory() as session:
            registros = session.scalars(
                select(RegistroContextoAgricola)
                .where(RegistroContextoAgricola.agricultor_id == id_a_entero(agricultor_id))
                .order_by(RegistroContextoAgricola.fecha_creacion.desc())
            ).all()
            return [self._a_entidad(registro) for registro in registros]

    def buscar_por_id_para_agricultor(
        self, contexto_id: str, agricultor_id: str
    ) -> ContextoAgricola | None:
        with self._session_factory() as session:
            registro = session.scalar(
                select(RegistroContextoAgricola).where(
                    RegistroContextoAgricola.id == id_a_entero(contexto_id),
                    RegistroContextoAgricola.agricultor_id == id_a_entero(agricultor_id),
                )
            )
            if registro is None:
                return None
            return self._a_entidad(registro)

    def seleccionar_para_agricultor(
        self, contexto_id: str, agricultor_id: str
    ) -> ContextoAgricola | None:
        with self._session_factory() as session:
            registro = session.scalar(
                select(RegistroContextoAgricola).where(
                    RegistroContextoAgricola.id == id_a_entero(contexto_id),
                    RegistroContextoAgricola.agricultor_id == id_a_entero(agricultor_id),
                )
            )
            if registro is None:
                return None
            session.execute(
                update(RegistroContextoAgricola)
                .where(RegistroContextoAgricola.agricultor_id == id_a_entero(agricultor_id))
                .values(esta_seleccionado=False)
            )
            registro.esta_seleccionado = True
            session.commit()
            session.refresh(registro)
            return self._a_entidad(registro)

    def _a_entidad(self, registro: RegistroContextoAgricola) -> ContextoAgricola:
        nombre = (registro.nombre_parcela or "").strip() or None
        observaciones = (registro.observaciones or "").strip() or None
        return ContextoAgricola(
            contexto_id=id_a_dominio(registro.id),
            agricultor_id=id_a_dominio(registro.agricultor_id),
            nombre_predio=nombre,
            cultivo=Cultivo(registro.cultivo),
            region=Region(registro.region),
            observaciones=observaciones,
            esta_seleccionado=bool(registro.esta_seleccionado),
            creado_en=registro.fecha_creacion,
        )
