"""Comportamiento del clasificador v2 sobre los anexos, sin reentrenar.

No exige abstención en todas las ambiguas. Una categoría temática en una
consulta fuera de alcance no es una detección de fuera de alcance.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from app.application.useCases.clasificar_consulta import ClasificarConsulta
from app.domain.ports.input.clasificar_consulta_port import ComandoClasificarConsulta
from app.domain.ports.output.puerto_clasificador_consultas import (
    CATEGORIAS_TEMATICAS_CONJUNTO,
    SALIDA_SIN_CATEGORIA,
)
from app.infrastructure.adapters.output.clasificacion.adaptador_clasificador_tfidf import (
    AdaptadorClasificadorTfidf,
    resolver_ruta_modelo,
)
from app.infrastructure.config.settings import Settings

UMBRAL = 0.17
BACKEND = Path(__file__).resolve().parents[1]
ANEXOS = BACKEND / "clasificacion" / "preparacion" / "dataset_trabajo_hu07"
AMBIGUA = ANEXOS / "cola_ambigua.jsonl"
FUERA = ANEXOS / "fuera_de_alcance.jsonl"


def _leer(path: Path) -> list[dict]:
    filas = []
    for linea in path.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            filas.append(json.loads(linea))
    return filas


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def clasificador() -> ClasificarConsulta:
    assert Settings.model_fields["clasificador_margen_minimo"].default == UMBRAL
    return ClasificarConsulta(
        AdaptadorClasificadorTfidf(resolver_ruta_modelo("")),
        UMBRAL,
    )


def _evaluar(clasificador: ClasificarConsulta, fila: dict, grupo: str) -> dict:
    resultado = clasificador.ejecutar(ComandoClasificarConsulta(texto=fila["text"]))
    repetido = clasificador.ejecutar(ComandoClasificarConsulta(texto=fila["text"]))
    return {
        "id": fila["id"],
        "grupo": grupo,
        "text": fila["text"],
        "categoria": resultado.categoria,
        "clase_primera": resultado.clase_primera,
        "clase_segunda": resultado.clase_segunda,
        "margen": resultado.margen,
        "abstencion": resultado.abstencion,
        "motivo": resultado.motivo_abstencion,
        "categoria_tematica_forzada": not resultado.abstencion,
        "reproducible": (
            resultado.categoria == repetido.categoria
            and resultado.abstencion == repetido.abstencion
            and resultado.clase_primera == repetido.clase_primera
            and resultado.clase_segunda == repetido.clase_segunda
            and resultado.margen == repetido.margen
        ),
    }


def _comprobar(fila_anexo: dict, evaluada: dict) -> None:
    assert evaluada["id"] == fila_anexo["id"]
    assert evaluada["text"] == fila_anexo["text"]
    assert evaluada["reproducible"] is True
    assert evaluada["clase_primera"] in CATEGORIAS_TEMATICAS_CONJUNTO
    assert evaluada["clase_segunda"] in CATEGORIAS_TEMATICAS_CONJUNTO
    assert SALIDA_SIN_CATEGORIA not in CATEGORIAS_TEMATICAS_CONJUNTO
    if evaluada["margen"] < UMBRAL:
        assert evaluada["abstencion"] is True
        assert evaluada["categoria"] == SALIDA_SIN_CATEGORIA
        assert evaluada["categoria_tematica_forzada"] is False
        assert evaluada["motivo"] == "margen_insuficiente"
    else:
        assert evaluada["abstencion"] is False
        assert evaluada["categoria"] == evaluada["clase_primera"]
        assert evaluada["categoria"] in CATEGORIAS_TEMATICAS_CONJUNTO
        assert evaluada["categoria_tematica_forzada"] is True
        assert evaluada["motivo"] is None


def test_anexos_conservan_dieciseis_y_doce() -> None:
    ambiguas = _leer(AMBIGUA)
    fuera = _leer(FUERA)
    assert len(ambiguas) == 16
    assert len(fuera) == 12
    assert len({fila["id"] for fila in ambiguas}) == 16
    assert len({fila["id"] for fila in fuera}) == 12
    assert all(fila["resolved_category"] == "" for fila in ambiguas)
    assert all(fila["proposed_category"] is None for fila in fuera)
    assert all(fila["disposition"] == "fuera_de_alcance" for fila in fuera)


def test_ambiguas_con_el_modelo_real(clasificador: ClasificarConsulta) -> None:
    modelo = resolver_ruta_modelo("")
    huella = _sha(modelo)
    for fila in _leer(AMBIGUA):
        _comprobar(fila, _evaluar(clasificador, fila, "ambigua"))
    assert _sha(modelo) == huella


def test_fuera_de_alcance_no_es_una_clase(clasificador: ClasificarConsulta) -> None:
    modelo = resolver_ruta_modelo("")
    huella = _sha(modelo)
    for fila in _leer(FUERA):
        evaluada = _evaluar(clasificador, fila, "fuera_de_alcance")
        _comprobar(fila, evaluada)
        assert evaluada["categoria"] != "fuera_de_alcance"
    clases = {
        str(clase)
        for clase in clasificador._puerto_clasificador._pipeline.named_steps["clf"].classes_
    }
    assert clases == CATEGORIAS_TEMATICAS_CONJUNTO
    assert "fuera_de_alcance" not in clases
    assert _sha(modelo) == huella
