import sys
import threading
from pathlib import Path

import numpy as np

from app.domain.exceptions import ErrorPredictorRiesgoNoDisponible
from app.domain.ports.output.puerto_predictor_riesgo import (
    CATEGORIAS_RIESGO_CONJUNTO,
    EscenarioRiesgo,
    PuertoPredictorRiesgo,
)

NOMBRE_MODELO = "modelo_riesgo_hu08.joblib"
RUTA_RELATIVA_MODELO = (
    Path("backend") / "clasificacion" / "experimentos" / "hu08_riesgo" / NOMBRE_MODELO
)
MENSAJE_CARGA = "No se pudo cargar el modelo de riesgo del prototipo HU-08."


def raiz_del_proyecto() -> Path:
    actual = Path(__file__).resolve()
    for candidato in actual.parents:
        if (candidato / "backend" / "app" / "main.py").is_file() and (
            candidato / RUTA_RELATIVA_MODELO.parent
        ).is_dir():
            return candidato
    raise ErrorPredictorRiesgoNoDisponible(
        "No se localizó la raíz del proyecto para ubicar el modelo de riesgo."
    )


def resolver_ruta_modelo_riesgo() -> Path:
    return raiz_del_proyecto() / RUTA_RELATIVA_MODELO


class AdaptadorPredictorRiesgo(PuertoPredictorRiesgo):
    """Carga el pipeline HU-08 una sola vez. No reentrena y no devuelve probabilidades."""

    def __init__(self, ruta_modelo: Path) -> None:
        self._ruta_modelo = ruta_modelo
        self._pipeline = None
        self._orden: tuple[str, ...] | None = None
        self._candado = threading.Lock()

    def predecir(self, escenario: EscenarioRiesgo) -> str:
        pipeline, orden = self._obtener_pipeline()
        fila = np.empty((1, len(orden)), dtype=object)
        valores = (
            escenario.familia_escenario,
            escenario.cultivo,
            escenario.region,
            escenario.etapa_fenologica,
            escenario.temperatura_c,
            escenario.precipitacion_mm,
            escenario.dias_sin_lluvia,
            escenario.sintoma_observado,
            escenario.proporcion_afectada,
            escenario.condicion_suelo,
        )
        if len(valores) != len(orden):
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
        for indice, valor in enumerate(valores):
            fila[0, indice] = valor
        try:
            prediccion = pipeline.predict(fila)
        except Exception as error:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA) from error
        if len(prediccion) != 1:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
        return str(prediccion[0])

    def _obtener_pipeline(self):
        if self._pipeline is not None and self._orden is not None:
            return self._pipeline, self._orden
        with self._candado:
            if self._pipeline is not None and self._orden is not None:
                return self._pipeline, self._orden
            self._pipeline, self._orden = self._cargar()
            return self._pipeline, self._orden

    def _cargar(self):
        if not self._ruta_modelo.is_file():
            raise ErrorPredictorRiesgoNoDisponible(
                "No se encuentra el modelo de riesgo HU-08 "
                f"({RUTA_RELATIVA_MODELO.as_posix()})."
            )
        try:
            import joblib
        except ImportError as error:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA) from error
        orden = self._importar_orden()
        try:
            modelo = joblib.load(self._ruta_modelo)
        except Exception as error:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA) from error
        self._validar(modelo, orden)
        return modelo, orden

    def _importar_orden(self) -> tuple[str, ...]:
        carpeta = str(self._ruta_modelo.parent)
        if carpeta not in sys.path:
            sys.path.insert(0, carpeta)
        try:
            import preprocesamiento_riesgo_hu08 as modulo
        except ImportError as error:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA) from error
        orden = tuple(modulo.ORDEN_VARIABLES)
        if orden != (
            "familia_escenario",
            "cultivo",
            "region",
            "etapa_fenologica",
            "temperatura_c",
            "precipitacion_mm",
            "dias_sin_lluvia",
            "sintoma_observado",
            "proporcion_afectada",
            "condicion_suelo",
        ):
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
        return orden

    def _validar(self, modelo, orden: tuple[str, ...]) -> None:
        del orden
        pasos = getattr(modelo, "named_steps", None)
        if not isinstance(pasos, dict) and not hasattr(pasos, "get"):
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
        clasificador = pasos.get("clasificador")
        if clasificador is None or not hasattr(clasificador, "classes_"):
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
        clases = {str(clase) for clase in clasificador.classes_}
        if clases != CATEGORIAS_RIESGO_CONJUNTO:
            raise ErrorPredictorRiesgoNoDisponible(MENSAJE_CARGA)
