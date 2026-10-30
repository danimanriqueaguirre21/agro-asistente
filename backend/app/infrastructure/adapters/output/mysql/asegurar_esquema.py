from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine


def sentencias_de_esquema(texto: str) -> list[str]:
    """Deja solo los CREATE TABLE. Aiven ya tiene defaultdb y no deja crear otra base."""
    corte = texto.find("SET @columna_titulo")
    if corte != -1:
        texto = texto[:corte]
    bloques: list[str] = []
    actual: list[str] = []
    saltar = False
    for linea in texto.splitlines():
        recortada = linea.strip()
        if not recortada or recortada.startswith("--"):
            continue
        mayusculas = recortada.upper()
        if mayusculas.startswith("CREATE DATABASE") or mayusculas.startswith("USE "):
            saltar = not recortada.endswith(";")
            continue
        if saltar:
            saltar = not recortada.endswith(";")
            continue
        actual.append(linea)
        if recortada.endswith(";"):
            bloques.append("\n".join(actual))
            actual = []
    return bloques


def ruta_esquema() -> Path:
    actual = Path(__file__).resolve()
    for padre in actual.parents:
        candidato = padre / "database" / "schema.sql"
        if candidato.is_file():
            return candidato
    raise FileNotFoundError("No se encontró database/schema.sql")


def asegurar_esquema(engine: Engine) -> None:
    texto = ruta_esquema().read_text(encoding="utf-8")
    with engine.begin() as conexion:
        for sentencia in sentencias_de_esquema(texto):
            conexion.execute(text(sentencia))
