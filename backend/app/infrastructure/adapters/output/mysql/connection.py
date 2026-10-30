import ssl

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.infrastructure.config.settings import Settings, get_settings


class Base(DeclarativeBase):
    """Declarative base de SQLAlchemy. Solo debe usarse en infraestructura MySQL."""


def argumentos_de_conexion(settings: Settings) -> dict:
    """Aiven pide TLS. El modo REQUIRED cifra sin exigir el certificado de la CA."""
    argumentos: dict = {"connect_timeout": 20 if settings.mysql_ssl else 3}
    if settings.mysql_ssl:
        contexto = ssl.create_default_context()
        contexto.check_hostname = False
        contexto.verify_mode = ssl.CERT_NONE
        argumentos["ssl"] = contexto
    return argumentos


def create_mysql_engine(settings: Settings | None = None) -> Engine:
    current = settings or get_settings()
    return create_engine(
        current.mysql_url,
        pool_pre_ping=True,
        future=True,
        connect_args=argumentos_de_conexion(current),
    )


def create_session_factory(settings: Settings | None = None) -> sessionmaker:
    engine = create_mysql_engine(settings)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def ping_mysql(settings: Settings | None = None) -> bool:
    try:
        engine = create_mysql_engine(settings)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except (SQLAlchemyError, OSError):
        return False


def id_a_entero(valor: str | int) -> int:
    return int(str(valor).strip())


def id_a_dominio(valor: int | str) -> str:
    return str(valor)
