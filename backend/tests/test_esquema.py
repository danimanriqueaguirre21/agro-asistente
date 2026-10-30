from app.infrastructure.adapters.output.mysql.asegurar_esquema import (
    ruta_esquema,
    sentencias_de_esquema,
)


def test_el_esquema_no_intenta_crear_otra_base() -> None:
    sentencias = sentencias_de_esquema(ruta_esquema().read_text(encoding="utf-8"))
    unidas = "\n".join(sentencias).upper()
    assert "CREATE DATABASE" not in unidas
    assert "CHARACTER SET" not in unidas
    assert "\nUSE " not in unidas
    assert any("CREATE TABLE IF NOT EXISTS agricultores" in sentencia for sentencia in sentencias)
    assert any("CREATE TABLE IF NOT EXISTS evidencias" in sentencia for sentencia in sentencias)
