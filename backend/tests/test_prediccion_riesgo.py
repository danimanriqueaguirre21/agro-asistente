from pathlib import Path

from fastapi.testclient import TestClient

from app.application.useCases.predecir_riesgo import PredecirRiesgoAgricola
from app.domain.exceptions import ErrorPredictorRiesgoNoDisponible
from app.domain.ports.input.predecir_riesgo_port import ComandoPredecirRiesgo
from app.domain.ports.output.puerto_predictor_riesgo import (
    CATEGORIAS_RIESGO_CONJUNTO,
    EscenarioRiesgo,
    PuertoPredictorRiesgo,
)
from app.infrastructure.adapters.output.riesgo.adaptador_predictor_riesgo import (
    AdaptadorPredictorRiesgo,
)
from app.main import app, container

client = TestClient(app)

ESCENARIO_VALIDO = {
    "familia_escenario": "meteorologico",
    "cultivo": "papa",
    "region": "Huancayo",
    "etapa_fenologica": "floracion",
    "temperatura_c": 2.0,
    "precipitacion_mm": 50.0,
    "dias_sin_lluvia": 1,
    "sintoma_observado": False,
    "proporcion_afectada": 0,
    "condicion_suelo": "adecuado",
}


def _encabezado() -> dict[str, str]:
    token = container.puerto_emisor_token.emitir_token(
        "agricultor-prueba-riesgo",
        {"email": "riesgo@example.com"},
    )
    return {"Authorization": f"Bearer {token}"}


def test_escenario_valido_devuelve_el_contrato() -> None:
    response = client.post("/api/v1/riesgo", json=ESCENARIO_VALIDO, headers=_encabezado())

    assert response.status_code == 200
    cuerpo = response.json()
    assert cuerpo["categoria_predicha"] in CATEGORIAS_RIESGO_CONJUNTO
    assert cuerpo["identificador_modelo"] == "bosque_aleatorio_profundidad12_hoja1"
    assert cuerpo["version_reglas"] == "sintetica-hu08-v1"
    assert cuerpo["naturaleza"] == "prototipo_academico_sintetico"
    assert cuerpo["es_riesgo_agricola_validado"] is False
    assert "probabilidad" not in cuerpo
    assert "predict_proba" not in cuerpo


def test_nulos_de_temperatura_y_precipitacion_se_aceptan() -> None:
    escenario = {
        **ESCENARIO_VALIDO,
        "familia_escenario": "plaga_enfermedad",
        "temperatura_c": None,
        "precipitacion_mm": None,
        "sintoma_observado": True,
        "proporcion_afectada": 0.4,
        "etapa_fenologica": "emergencia",
    }

    response = client.post("/api/v1/riesgo", json=escenario, headers=_encabezado())

    assert response.status_code == 200
    assert response.json()["categoria_predicha"] in CATEGORIAS_RIESGO_CONJUNTO


def test_tipo_invalido_se_rechaza() -> None:
    escenario = {**ESCENARIO_VALIDO, "dias_sin_lluvia": "quince"}

    response = client.post("/api/v1/riesgo", json=escenario, headers=_encabezado())

    assert response.status_code == 422
    assert "categoria_predicha" not in response.json()


def test_proporcion_sin_sintoma_se_rechaza() -> None:
    escenario = {**ESCENARIO_VALIDO, "sintoma_observado": False, "proporcion_afectada": 0.2}

    response = client.post("/api/v1/riesgo", json=escenario, headers=_encabezado())

    assert response.status_code == 422


def test_sin_token_responde_401() -> None:
    response = client.post("/api/v1/riesgo", json=ESCENARIO_VALIDO)

    assert response.status_code == 401


def test_modelo_ausente_no_inventa_categoria() -> None:
    original = container.puerto_predecir_riesgo
    container.puerto_predecir_riesgo = PredecirRiesgoAgricola(
        AdaptadorPredictorRiesgo(Path("backend") / "clasificacion" / "experimentos" / "hu08_riesgo" / "modelo_inexistente.joblib")
    )
    try:
        response = client.post("/api/v1/riesgo", json=ESCENARIO_VALIDO, headers=_encabezado())
    finally:
        container.puerto_predecir_riesgo = original

    assert response.status_code == 503
    assert "categoria_predicha" not in response.json()


def test_predictor_falso_mantiene_el_contrato() -> None:
    class _Fijo(PuertoPredictorRiesgo):
        def predecir(self, escenario: EscenarioRiesgo) -> str:
            return "medio"

    resultado = PredecirRiesgoAgricola(_Fijo()).ejecutar(
        ComandoPredecirRiesgo(
            escenario=EscenarioRiesgo(
                familia_escenario="suelo_agua_manejo",
                cultivo="quinua",
                region="Jauja",
                etapa_fenologica="siembra",
                temperatura_c=None,
                precipitacion_mm=None,
                dias_sin_lluvia=0,
                sintoma_observado=False,
                proporcion_afectada=0,
                condicion_suelo="adecuado",
            )
        )
    )

    assert resultado.categoria_predicha == "medio"
    assert resultado.es_riesgo_agricola_validado is False
    assert resultado.naturaleza == "prototipo_academico_sintetico"


def test_categoria_fuera_del_prototipo_no_se_entrega() -> None:
    class _Ajena(PuertoPredictorRiesgo):
        def predecir(self, escenario: EscenarioRiesgo) -> str:
            return "critico"

    caso = PredecirRiesgoAgricola(_Ajena())
    escenario = EscenarioRiesgo(
        familia_escenario="meteorologico",
        cultivo="papa",
        region="Huancayo",
        etapa_fenologica="floracion",
        temperatura_c=None,
        precipitacion_mm=10,
        dias_sin_lluvia=2,
        sintoma_observado=False,
        proporcion_afectada=0,
        condicion_suelo="adecuado",
    )
    try:
        caso.ejecutar(ComandoPredecirRiesgo(escenario=escenario))
    except ErrorPredictorRiesgoNoDisponible:
        return
    raise AssertionError("Se entregó una categoría que no pertenece al prototipo.")


def test_rutas_existentes_siguen_expuestas() -> None:
    esquema = client.get("/openapi.json")
    assert esquema.status_code == 200
    rutas = esquema.json()["paths"]
    assert "/health" in rutas
    assert "/api/v1/queries" in rutas
    assert "/api/v1/clasificacion" in rutas
    assert "/api/v1/riesgo" in rutas
    assert client.get("/health").status_code == 200
    assert client.post("/api/v1/clasificacion", json={"text": "¿Cómo riego la papa?"}).status_code == 401
    assert client.post("/api/v1/queries", json={"text": "¿Cómo riego la papa?"}).status_code == 401
