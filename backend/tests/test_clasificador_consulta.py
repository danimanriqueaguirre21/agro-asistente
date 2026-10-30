from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.application.useCases.clasificar_consulta import ClasificarConsulta, decidir_clasificacion
from app.domain.exceptions import ErrorClasificadorNoDisponible, ErrorTextoConsultaInvalido
from app.domain.ports.input.clasificar_consulta_port import ComandoClasificarConsulta
from app.domain.ports.output.puerto_clasificador_consultas import (
    CATEGORIAS_TEMATICAS_CONJUNTO,
    SALIDA_SIN_CATEGORIA,
    PuertoClasificadorConsultas,
    PuntuacionModelo,
)
from app.infrastructure.adapters.output.clasificacion.adaptador_clasificador_tfidf import (
    NOMBRE_MODELO,
    AdaptadorClasificadorTfidf,
    resolver_ruta_modelo,
)
from app.infrastructure.config.settings import Settings
from app.main import app

UMBRAL = 0.17
CONSULTA_AGRICOLA = "¿Dejo correr el agua por el surco del ajo hasta el final del cantero?"


class _PuertoFijo(PuertoClasificadorConsultas):
    def __init__(self, puntuacion: PuntuacionModelo) -> None:
        self.puntuacion = puntuacion
        self.llamadas = 0

    def puntuar(self, texto: str) -> PuntuacionModelo:
        self.llamadas += 1
        return self.puntuacion


def test_settings_rechaza_un_umbral_fuera_de_rango() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, clasificador_margen_minimo=1.5)


def test_consulta_vacia_no_llama_al_modelo() -> None:
    puerto = _PuertoFijo(
        PuntuacionModelo("riego", 0.8, "suelos", 0.1)
    )
    caso = ClasificarConsulta(puerto, UMBRAL)

    with pytest.raises(ErrorTextoConsultaInvalido):
        caso.ejecutar(ComandoClasificarConsulta(texto="   "))

    assert puerto.llamadas == 0


def test_abstencion_cuando_el_margen_es_menor_que_el_umbral() -> None:
    resultado = decidir_clasificacion(
        PuntuacionModelo("riego", 0.40, "suelos", 0.30),
        UMBRAL,
    )

    assert resultado.abstencion is True
    assert resultado.categoria == SALIDA_SIN_CATEGORIA
    assert resultado.motivo_abstencion == "margen_insuficiente"
    assert resultado.margen < UMBRAL
    assert resultado.puntuaciones_calibradas is False
    assert resultado.clase_primera in CATEGORIAS_TEMATICAS_CONJUNTO
    assert SALIDA_SIN_CATEGORIA not in CATEGORIAS_TEMATICAS_CONJUNTO


def test_clasifica_cuando_el_margen_es_igual_al_corte() -> None:
    puntuacion = PuntuacionModelo("plagas", 0.70, "enfermedades_cultivos", 0.53)
    corte = puntuacion.puntuacion_primera - puntuacion.puntuacion_segunda
    resultado = decidir_clasificacion(puntuacion, corte)

    assert resultado.abstencion is False
    assert resultado.categoria == "plagas"
    assert resultado.motivo_abstencion is None
    assert resultado.margen == corte
    assert resultado.categoria in CATEGORIAS_TEMATICAS_CONJUNTO


def test_clasifica_cuando_el_margen_supera_el_umbral() -> None:
    resultado = decidir_clasificacion(
        PuntuacionModelo("cosecha_poscosecha", 0.80, "clima_heladas", 0.10),
        UMBRAL,
    )

    assert resultado.abstencion is False
    assert resultado.categoria == "cosecha_poscosecha"
    assert resultado.margen >= UMBRAL


def test_una_salida_ajena_a_las_ocho_no_se_acepta() -> None:
    with pytest.raises(ErrorClasificadorNoDisponible):
        decidir_clasificacion(
            PuntuacionModelo(SALIDA_SIN_CATEGORIA, 0.9, "riego", 0.1),
            UMBRAL,
        )


def test_modelo_ausente_devuelve_error_controlado(tmp_path: Path) -> None:
    adaptador = AdaptadorClasificadorTfidf(tmp_path / "no-existe.joblib")

    with pytest.raises(ErrorClasificadorNoDisponible, match="No se encuentra el modelo"):
        adaptador.puntuar(CONSULTA_AGRICOLA)


def test_carga_el_modelo_v2_y_predice_una_de_las_ocho() -> None:
    ruta = resolver_ruta_modelo("")
    assert ruta.name == NOMBRE_MODELO
    assert ruta.is_file()
    assert ruta.as_posix().endswith(
        "backend/clasificacion/experimentos/hu07_tfidf_v2/modelo_tfidf_logreg_v2.joblib"
    )

    adaptador = AdaptadorClasificadorTfidf(ruta)
    primera = adaptador.puntuar(CONSULTA_AGRICOLA)
    segunda = adaptador.puntuar(CONSULTA_AGRICOLA)

    assert primera.clase_primera in CATEGORIAS_TEMATICAS_CONJUNTO
    assert primera.clase_segunda in CATEGORIAS_TEMATICAS_CONJUNTO
    assert primera.clase_primera != SALIDA_SIN_CATEGORIA
    assert segunda.clase_primera == primera.clase_primera
    clases = set(adaptador._pipeline.named_steps["clf"].classes_)
    assert {str(clase) for clase in clases} == CATEGORIAS_TEMATICAS_CONJUNTO
    assert SALIDA_SIN_CATEGORIA not in {str(clase) for clase in clases}


def test_la_consulta_clasifica_una_vez_y_conserva_rutas_y_ollama() -> None:
    registrar = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "application"
        / "useCases"
        / "registrar_consulta.py"
    ).read_text(encoding="utf-8")
    assert registrar.count("self._clasificar_consulta.ejecutar") == 1
    assert "recuperar(consulta.texto.value)" in registrar
    ollama = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "infrastructure"
        / "adapters"
        / "output"
        / "generation"
        / "adaptador_generacion_ollama.py"
    ).read_text(encoding="utf-8").lower()
    assert "clasificador" not in ollama
    assert "sin categoría" not in ollama

    esquema = TestClient(app).get("/openapi.json")
    assert esquema.status_code == 200
    rutas = set(esquema.json()["paths"])
    assert "/health" in rutas
    assert "/api/v1/queries" in rutas
    assert "/api/v1/clasificacion" in rutas

    response = TestClient(app).post("/api/v1/clasificacion", json={"text": CONSULTA_AGRICOLA})
    assert response.status_code == 401
    consulta = TestClient(app).post("/api/v1/queries", json={"text": CONSULTA_AGRICOLA})
    assert consulta.status_code == 401
