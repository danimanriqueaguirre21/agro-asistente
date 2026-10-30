import threading
from pathlib import Path

from app.domain.exceptions import ErrorClasificadorNoDisponible
from app.domain.ports.output.puerto_clasificador_consultas import (
    CATEGORIAS_TEMATICAS_CONJUNTO,
    SALIDA_SIN_CATEGORIA,
    PuertoClasificadorConsultas,
    PuntuacionModelo,
)

NOMBRE_MODELO = "modelo_tfidf_logreg_v2.joblib"
RUTA_RELATIVA_MODELO = Path("backend") / "clasificacion" / "experimentos" / "hu07_tfidf_v2" / NOMBRE_MODELO


def raiz_del_proyecto() -> Path:
    actual = Path(__file__).resolve()
    for candidato in actual.parents:
        if (candidato / "backend" / "app" / "main.py").is_file() and (
            candidato / RUTA_RELATIVA_MODELO.parent
        ).is_dir():
            return candidato
    raise ErrorClasificadorNoDisponible(
        "No se localizó la raíz del proyecto para ubicar el clasificador."
    )


def resolver_ruta_modelo(ruta_configurada: str) -> Path:
    texto = (ruta_configurada or "").strip()
    if not texto:
        return raiz_del_proyecto() / RUTA_RELATIVA_MODELO
    ruta = Path(texto)
    if ruta.is_absolute():
        return ruta
    return raiz_del_proyecto() / ruta


class AdaptadorClasificadorTfidf(PuertoClasificadorConsultas):
    """Carga el pipeline v2 una sola vez. No reentrena y no aplica el umbral."""

    def __init__(self, ruta_modelo: Path) -> None:
        self._ruta_modelo = ruta_modelo
        self._pipeline = None
        self._candado = threading.Lock()

    def puntuar(self, texto: str) -> PuntuacionModelo:
        pipeline = self._obtener_pipeline()
        probabilidades = pipeline.predict_proba([texto])[0]
        clases = [str(clase) for clase in pipeline.named_steps["clf"].classes_]
        orden = sorted(range(len(clases)), key=lambda indice: float(probabilidades[indice]), reverse=True)
        primera = orden[0]
        segunda = orden[1]
        return PuntuacionModelo(
            clase_primera=clases[primera],
            puntuacion_primera=float(probabilidades[primera]),
            clase_segunda=clases[segunda],
            puntuacion_segunda=float(probabilidades[segunda]),
        )

    def _obtener_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline
        with self._candado:
            if self._pipeline is not None:
                return self._pipeline
            self._pipeline = self._cargar()
            return self._pipeline

    def _cargar(self):
        if not self._ruta_modelo.is_file():
            raise ErrorClasificadorNoDisponible(
                "No se encuentra el modelo v2 del clasificador "
                f"({RUTA_RELATIVA_MODELO.as_posix()})."
            )
        try:
            import joblib
        except ImportError as exc:
            raise ErrorClasificadorNoDisponible(
                "joblib no está disponible para cargar el clasificador."
            ) from exc
        try:
            modelo = joblib.load(self._ruta_modelo)
        except Exception as exc:
            raise ErrorClasificadorNoDisponible(
                "No se pudo cargar el modelo v2 del clasificador."
            ) from exc
        self._validar(modelo)
        return modelo

    def _validar(self, modelo) -> None:
        pasos = getattr(modelo, "named_steps", None)
        if pasos is None or not hasattr(pasos, "get"):
            raise ErrorClasificadorNoDisponible(
                "El archivo del clasificador no es el pipeline esperado."
            )
        clasificador = pasos.get("clf")
        if clasificador is None or not hasattr(clasificador, "classes_"):
            raise ErrorClasificadorNoDisponible(
                "El pipeline del clasificador no tiene el paso clf."
            )
        encontradas = {str(clase) for clase in clasificador.classes_}
        if SALIDA_SIN_CATEGORIA in encontradas:
            raise ErrorClasificadorNoDisponible(
                "sin categoría no puede ser una clase del modelo."
            )
        if encontradas != CATEGORIAS_TEMATICAS_CONJUNTO:
            raise ErrorClasificadorNoDisponible(
                "El modelo no contiene exactamente las ocho categorías temáticas."
            )
